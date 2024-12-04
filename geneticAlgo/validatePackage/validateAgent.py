import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from runWithADP import *

# Database connection details
user = 'admin'
password = 'fillerpassword'
host = 'fantasy-football-ai.c180k46m8sh9.us-east-1.rds.amazonaws.com'
database_name = 'fantasyfootballproject'

# Function to generate SQL query for a specific year
def generate_query(year):
    return f"""
    WITH articles (playerId, avgArticleScore, season) AS (
        SELECT 
            playerId, 
            AVG(articleScore) as avgArticleScore, 
            YEAR(date) AS season 
        FROM 
            fantasyfootballproject.articles 
        GROUP BY 
            playerId, season
    )
    SELECT 
        playerName, pid, position, passing.year, height, weight, age, injuries, adp, totalPoints, 
        passingYards, attempts, completions, interceptions, sacks, passingTDs, passing2Pts, 
        receptions, targets, receivingYards, receivingTDs, receiving2Pts, rushingYards, 
        carries, rushingTDs, rushing2Pts, fumbles, avgArticleScore 
    FROM 
        fantasyfootballproject.players p
    INNER JOIN 
        fantasyfootballproject.passing passing ON (p.pid = passing.playerId)
    INNER JOIN 
        fantasyfootballproject.receiving rec ON (passing.playerId = rec.playerId AND passing.year = rec.year)
    INNER JOIN 
        fantasyfootballproject.rushing rush ON (rec.playerId = rush.playerId AND rec.year = rush.year)
    INNER JOIN 
        fantasyfootballproject.fumbles f ON (f.playerId = rush.playerId AND f.year = rush.year)
    INNER JOIN 
        fantasyfootballproject.playerRankingByYear prby ON (passing.playerId = prby.playerId AND passing.year = prby.year)
    LEFT JOIN 
        articles a ON (a.playerId = prby.playerId AND passing.year = a.season)
    WHERE 
        passing.year = {year};
    """

# Connect to the database and fetch data
def fetch_data_from_aws(query):
    try:
        connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database_name}"
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Load the best agent weights from an Excel file
def load_best_agent(file_path):
    return pd.read_excel(file_path).iloc[0].to_dict()  # Assuming weights are in the first row

def violates_min_constraints(position_counts, pos):
    """
    Check if selecting a player for a position would prevent meeting the minimum constraints.
    """
    position_counts_temp = position_counts.copy()
    position_counts_temp[pos] += 1  # Simulate selecting this position

    for p, (min_count, max_count) in position_constraints.items():
        if position_counts_temp[p] < min_count:  # Ensure min constraint is still achievable
            return True
    return False

# Select team with validation and calculate agentScore
def select_team_validate(agent_weights, players, pick_order):
    team = []
    position_counts = {pos: 0 for pos in position_constraints}
    selected_player_ids = set()

    for i, round_pick in enumerate(pick_order):
        if len(team) >= 14:  # Stop if the team already has 14 players
            break

        # Filter players based on ADP and ensure they are not already selected
        filtered_players = [
            p for p in players if p["adp"] >= round_pick and p["pid"] not in selected_player_ids
        ]

        # If no players match, include fallback logic for players with ADP = -1
        if not filtered_players:
            print(f"No players matched the ADP criteria at Pick Order {round_pick}. Checking players with ADP = -1.")
            filtered_players = [
                p for p in players if p["adp"] == -1 and p["pid"] not in selected_player_ids
            ]

        # If still no players match, expand filter to include all remaining players
        if not filtered_players:
            print(f"No players matched ADP = -1. Expanding to include all unselected players.")
            filtered_players = [p for p in players if p["pid"] not in selected_player_ids]

        # Calculate agentScore for filtered players
        scored_players = [
            (player, calculate_agent_score(player, agent_weights))
            for player in filtered_players
        ]

        # Add agentScore to player data for output
        for player, score in scored_players:
            player["agentScore"] = score

        # Sort players by agentScore in descending order
        sorted_players = sorted(scored_players, key=lambda x: x[1], reverse=True)

        # Select the best player who satisfies positional constraints
        if sorted_players:
            for player, _ in sorted_players:
                pos = player["position"]
                # Check if selecting this player satisfies constraints
                if position_counts[pos] < position_constraints[pos][1]:
                    # Ensure selecting this player does not block meeting minimum constraints
                    print(f"Selected Player: {player['playerName']} (Position: {player['position']}, Agent Score: {player['agentScore']})")
                    team.append(player)
                    position_counts[pos] += 1
                    selected_player_ids.add(player["pid"])
                    break
            print(f"Position Counts After Pick {i}: {position_counts}")

    # Final Validation: Check if Constraints Are Satisfied
    if satisfies_constraints(team):
        print(f"Final Team Satisfies Constraints: {[p['playerName'] for p in team]}")
        return team[:14]

    # If constraints are not satisfied, fallback to best 14 players by agentScore
    print("Constraints not satisfied. Falling back to best 14 players.")
    remaining_players = [
        p for p in players if p["pid"] not in selected_player_ids
    ]
    scored_remaining = [
        (player, calculate_agent_score(player, agent_weights))
        for player in remaining_players
    ]
    for player, score in scored_remaining:
        player["agentScore"] = score
    fallback_team = sorted(scored_remaining, key=lambda x: x[1], reverse=True)[:14]
    print(f"Fallback Team: {[p['playerName'] for p, _ in fallback_team]}")
    return [player for player, _ in fallback_team]


# Visualization function
def visualize_comparison(optimized_score, adp_score, optimized_team, adp_team):
    # Plot bar chart for total scores
    categories = ['Optimized Team', 'ADP Reference Team']
    scores = [optimized_score, adp_score]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, scores, color=['blue', 'green'], alpha=0.7)
    plt.title('Agent Optimized Team vs ADP Reference Team', fontsize=14)
    plt.ylabel('Total Points', fontsize=12)
    plt.xlabel('Team Type', fontsize=12)

    # Annotate scores on top of the bars
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 10,
                 f'{score}', ha='center', va='bottom', fontsize=12, color='white', weight='bold')

    # Pick-by-pick player-level comparison
    plt.figure(figsize=(12, 8))
    num_picks = len(optimized_team)
    picks = range(1, num_picks + 1)

    # Points from Optimized Team and ADP Reference Team
    optimized_points = [player['totalPoints'] for player in optimized_team]
    adp_points = [player['totalPoints'] for player in adp_team]

    plt.plot(picks, optimized_points, label="Optimized Team", marker='o', color='blue', alpha=0.7)
    plt.plot(picks, adp_points, label="ADP Reference Team", marker='o', color='green', alpha=0.7)

    # Annotate player names on each pick
    for i, (opt_player, adp_player) in enumerate(zip(optimized_team, adp_team)):
        plt.text(i + 1, optimized_points[i], f"{opt_player['playerName']}", fontsize=8, ha='left', color='blue')
        plt.text(i + 1, adp_points[i], f"{adp_player['playerName']}", fontsize=8, ha='right', color='green')

    plt.title('Pick-by-Pick Player-Level Comparison', fontsize=14)
    plt.xlabel('Pick Number', fontsize=12)
    plt.ylabel('Total Points', fontsize=12)
    plt.xticks(picks)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



# Main function to validate the best agent
def validate_best_agent():
    query = generate_query(2023)
    data_2023 = fetch_data_from_aws(query)

    if data_2023 is None or data_2023.empty:
        print("Failed to fetch 2023 data.")
        return

    # Handle missing values for avgArticleScore
    data_2023.fillna({'avgArticleScore': 0.51746529}, inplace=True)
    print("Missing values for 'avgArticleScore' handled successfully.")
    data_2023.to_excel("2023_source_data_with_handled_missing_values.xlsx", index=False)
    print("2023 source data saved to 2023_source_data_with_handled_missing_values.xlsx.")

    best_agent_file = "recommended_agent_weights.xlsx"
    best_agent = load_best_agent(best_agent_file)
    print("Best Agent Weights:", best_agent)

    pick_order = [1, 24, 25, 48, 49, 72, 73, 96, 97, 120, 121, 144, 145, 168]

    # Generate optimized team
    optimized_team = select_team_validate(best_agent, data_2023.to_dict(orient="records"), pick_order)
    optimized_score = sum(player["totalPoints"] for player in optimized_team)

    # Generate ADP reference team
    adp_team = select_adp_reference_team(data_2023.to_dict(orient="records"), pick_order)
    adp_score = sum(player["totalPoints"] for player in adp_team)

    # Add pick order and agentScore to output
    for i, player in enumerate(optimized_team):
        player["Team Type"] = "Optimized"
        player["pickOrder"] = pick_order[i] if i < len(pick_order) else None

    for i, player in enumerate(adp_team):
        player["Team Type"] = "ADP Reference"
        player["pickOrder"] = pick_order[i] if i < len(pick_order) else None

    combined_teams = optimized_team + adp_team

    save_to_excel(combined_teams, "comparison_teams_2023_with_agentScore.xlsx")

    print(f"Optimized Team Score: {optimized_score}")
    print(f"ADP Reference Team Score: {adp_score}")

    # Visualize the comparison
    visualize_comparison(optimized_score, adp_score, optimized_team, adp_team)

    return {
        "optimized_team": optimized_team,
        "adp_team": adp_team,
        "optimized_score": optimized_score,
        "adp_score": adp_score,
    }

if __name__ == "__main__":
    results = validate_best_agent()
    print("Validation complete. Results saved to comparison_teams_2023_with_agentScore.xlsx")
