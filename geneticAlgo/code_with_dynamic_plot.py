# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:26:06 2024

@author: abc
"""

import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython import display

# Step 1: Debugging Functions
def debug_agent_scores(agent_weights, players):
    print("Agent Weights:", agent_weights)
    for player in players[:10]:  # Limit to first 10 players for readability
        score = calculate_agent_score(player, agent_weights)
        print(f"Player: {player['playerName']}, Agent Score: {score}")

def debug_selected_team(agent_weights, players, pick_order):
    team = select_team(agent_weights, players, pick_order)
    print("Selected Team:")
    for player in team:
        print(f"  {player['playerName']} (Position: {player['position']}, Total Points: {player['totalPoints']}, ADP: {player['adp']})")
    return team

# Step 2: Load Player Data
def load_combined_player_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Step 3: Define Constraints
position_constraints = {
    1: (1, 3),  # Min 1, Max 3 QB
    2: (2, 5),  # Min 2, Max 5 RB
    3: (2, 5),  # Min 2, Max 5 WR
    4: (1, 3),  # Min 1, Max 3 TE
}

def satisfies_constraints(team):
    position_counts = {pos: 0 for pos in position_constraints}
    for player in team:
        position_counts[player["position"]] += 1
    return all(position_counts[pos] >= position_constraints[pos][0] for pos in position_constraints)

# Step 4: Calculate Agent Score for Each Player
def calculate_agent_score(player, agent_weights):
    return sum(agent_weights[key] * player[key] for key in agent_weights if key in player and isinstance(player[key], (int, float)))

# Step 5: Team Selection with ADP and Position Constraints
def select_team(agent_weights, players, pick_order):
    team = []
    position_counts = {pos: 0 for pos in position_constraints}
    selected_player_ids = set()  # Track selected players to avoid duplicates

    for i, round_pick in enumerate(pick_order):
        # For the first pick, there are no ADP constraints
        if i == 0:
            filtered_players = [
                p for p in players if p["pid"] not in selected_player_ids
            ]
        else:
            # Apply ADP constraint for subsequent picks
            filtered_players = [
                p for p in players 
                if p["adp"] >= round_pick and p["pid"] not in selected_player_ids
            ]

        # Calculate scores for the filtered players
        scored_players = [
            (player, calculate_agent_score(player, agent_weights)) 
            for player in filtered_players
        ]

        # Sort by agent score (highest first)
        sorted_players = sorted(scored_players, key=lambda x: x[1], reverse=True)

        # Select the top player who fits positional constraints
        for player, _ in sorted_players:
            pos = player["position"]
            if position_counts[pos] < position_constraints[pos][1]:  # Check max constraint
                team.append(player)
                position_counts[pos] += 1
                selected_player_ids.add(player["pid"])  # Mark as selected
                break  # Proceed to the next pick
    return team if satisfies_constraints(team) else []

# Select ADP Reference Team
def select_adp_reference_team(players, pick_order):
    adp_team = []
    selected_player_ids = set()

    for round_pick in pick_order:
        filtered_players = [
            player for player in players if player["pid"] not in selected_player_ids and player["adp"] > 0
        ]
        if not filtered_players:
            continue

        closest_player = min(filtered_players, key=lambda p: abs(p["adp"] - round_pick))
        adp_team.append(closest_player)
        selected_player_ids.add(closest_player["pid"])

    return adp_team

# Step 6: Fitness Function
def calculate_team_score(team):
    return sum(player["totalPoints"] for player in team)

# Step 7: Genetic Algorithm Operations
def generate_initial_population(pop_size, attribute_keys):
    return [{key: random.uniform(0, 1) for key in attribute_keys} for _ in range(pop_size)]

def crossover(parent1, parent2):
    return {key: (parent1[key] + parent2[key]) / 2 for key in parent1}

def mutate(agent_weights, mutation_rate=0.1):
    for key in agent_weights:
        if random.random() < mutation_rate:
            agent_weights[key] = random.uniform(0, 1)

def inject_random_agents(population, pop_size, attribute_keys, injection_rate=0.1):
    num_random_agents = int(pop_size * injection_rate)
    random_agents = generate_initial_population(num_random_agents, attribute_keys)
    population.extend(random_agents)
    return population

# Save to Excel
def save_to_excel(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}.")

# Step 8: Run Genetic Algorithm Across All Years
def genetic_algorithm_across_years(data, pick_order, pop_size=50, generations_per_year=100):
    attribute_keys = [
        "height", "weight", "age", "injuries", "passingYards", "attempts", "completions",
        "interceptions", "sacks", "passingTDs", "passing2Pts", "receptions", "targets",
        "receivingYards", "receivingTDs", "receiving2Pts", "rushingYards", "carries",
        "rushingTDs", "rushing2Pts", "fumbles", "avgArticleScore"
    ]
    population = generate_initial_population(pop_size, attribute_keys)
    historical_best_agent = None
    historical_best_fitness = float('-inf')
    all_teams = []  # To save teams for each year
    adp_reference_teams = []  # To save reference teams for each year
    comparison_results = {}  # To store comparison results for each year
    agent_history = []
    generations_history = []
    temp_year=['2018'] #remove this later

    for year in sorted(data["year"].unique()):
    #for year in sorted(temp_year):  #remove this 
        print(f"Running genetic algorithm for year {year}...")
        year_data = data[data["year"] == year].to_dict(orient="records")
        max_total_points_year = max(player["totalPoints"] for player in year_data)

        for generation in range(generations_per_year):
            raw_fitness_scores = [
                calculate_team_score(select_team(agent, year_data, pick_order))
                for agent in population
            ]

            fitness_scores = [score / max_total_points_year for score in raw_fitness_scores]

            sorted_population = sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)
            best_fitness = sorted_population[0][0]

            best_raw_fitness = raw_fitness_scores[fitness_scores.index(best_fitness)]
            if best_raw_fitness > historical_best_fitness:
                historical_best_fitness = best_raw_fitness
                historical_best_agent = sorted_population[0][1]

            elite_agent = sorted_population[0][1]
            population = [elite_agent] + [x[1] for x in sorted_population[:pop_size // 2 - 1]]
            while len(population) < pop_size:
                parent1, parent2 = random.choices([x[1] for x in sorted_population[:pop_size // 2]], k=2)
                child = crossover(parent1, parent2)
                mutate(child, mutation_rate=0.1)
                population.append(child)
            
            #for plotting purpose
            best_generational_agent = sorted_population[0][1]
            #best_generational_team = select_team(best_generational_agent, year_data, pick_order)
            #for i, player in enumerate(best_generational_team):
                #player["pickOrder"] = pick_order[i]
                #player["year"] = year
            #all_teams.extend(best_generational_team)
            # Calculate optimized team score
            optimized_generational_team = select_team(best_generational_agent, year_data, pick_order)
            optimized_generational_score = calculate_team_score(optimized_generational_team)
            
            agent_history.append(optimized_generational_score)
            generations_history.append(generation + 1)

        best_agent = sorted_population[0][1]
        best_team = select_team(best_agent, year_data, pick_order)
        for i, player in enumerate(best_team):
            player["pickOrder"] = pick_order[i]
            player["year"] = year
        all_teams.extend(best_team)

        adp_team = select_adp_reference_team(year_data, pick_order)
        adp_reference_teams.extend(adp_team)
        adp_score = calculate_team_score(adp_team)

        # Calculate optimized team score
        optimized_team = select_team(best_agent, year_data, pick_order)
        optimized_score = calculate_team_score(optimized_team)

        # Store scores for the year
        comparison_results[year] = {"optimized_score": optimized_score, "adp_score": adp_score}

        print(f"Year {year} complete! Optimized Team Score: {optimized_score}, ADP Team Score: {adp_score}")

    save_to_excel(all_teams, "picked_teams_by_year.xlsx")
    save_to_excel(adp_reference_teams, "adp_reference_teams.xlsx")
    save_to_excel([historical_best_agent], "recommended_agent_weights.xlsx")
    save_to_excel(comparison_results, "team_comparison_results.xlsx")
    return historical_best_agent, comparison_results, agent_history, generations_history


def visualize_team_comparison(comparison_results):
    """
    Visualize the totalPoints comparison between the optimized team and the ADP reference team.
    
    :param comparison_results: A dictionary containing year-wise comparison of optimized and ADP team scores.
    """
    years = list(comparison_results.keys())
    optimized_scores = [comparison_results[year]["optimized_score"] for year in years]
    adp_scores = [comparison_results[year]["adp_score"] for year in years]

    x = np.arange(len(years))  # The label locations

    plt.figure(figsize=(10, 6))
    width = 0.35  # The width of the bars

    # Bar plot for Optimized Scores
    plt.bar(x - width / 2, optimized_scores, width, label="Optimized Team Score")

    # Bar plot for ADP Scores
    plt.bar(x + width / 2, adp_scores, width, label="ADP Reference Team Score")

    # Add labels, title, and legend
    plt.xlabel("Year")
    plt.ylabel("Total Points")
    plt.title("Comparison of Total Points: Optimized Team vs ADP Reference Team")
    plt.xticks(x, years)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def dynamic_plot(list_1, list_2, interval):
    """
    Function to dynamically plot data from list_1 (y-values) and list_2 (x-values).
    
    Parameters:
    - list_1: List of y-values to plot
    - list_2: List of x-values to plot
    - interval: Time interval (in seconds) between updating each point
    """
    # Create the figure and axis
    fig, ax = plt.subplots()
    hdisplay = display.display("", display_id=True)

    # Set labels and initial limits
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_xlim(0, max(list_2))
    ax.set_ylim(0, max(list_1))

    # Initialize empty data lists
    x_data = []
    y_data = []

    # Function to update the plot
    def update_plot(ax, x_data, y_data, hdisplay):
        if ax.lines:
            # Update existing line data
            ax.lines[0].set_xdata(x_data)
            ax.lines[0].set_ydata(y_data)
        else:
            # Plot initial data with adjustments
            ax.plot(x_data, y_data, '.-', lw=0.5, markersize=2, alpha=0.8)  # Adjusted line style
        
        # Update the display
        hdisplay.update(fig)
        ax.relim()
        ax.autoscale_view()

    # Plot each point iteratively
    for i in range(len(list_2)):
        x_data.append(list_2[i])
        y_data.append(list_1[i])
        
        update_plot(ax, x_data, y_data, hdisplay)
        time.sleep(interval)  # Pause for the specified interval

    plt.close(fig)  # Close the figure after updating

    
    # Main execution
if __name__ == "__main__":
    combined_file_path = "C://Users//abc//Desktop//combined_player_data_2012_2022.csv"
    data = load_combined_player_data(combined_file_path)
    pick_order = [1, 24, 25, 48, 49, 72, 73, 96, 97, 120, 121, 144, 145, 168]

    best_agent, comparison_results, agent_history, generations_history = genetic_algorithm_across_years(data, pick_order, pop_size=50, generations_per_year=100)
    
    # function to show model progress
    dynamic_plot(agent_history, generations_history, interval=0.12)
    
    # Visualize the team comparison
    visualize_team_comparison(comparison_results)

    with open("best_agent_across_years.txt", "w") as f:
        f.write(str(best_agent))