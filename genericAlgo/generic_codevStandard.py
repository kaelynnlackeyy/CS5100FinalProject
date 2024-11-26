import pandas as pd
import random
import numpy as np

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

def debug_population_diversity(population):
    unique_agents = len(set(tuple(agent.items()) for agent in population))
    print(f"Unique Agents in Population: {unique_agents}")

def debug_fitness_scores(fitness_scores):
    print("Top 5 Fitness Scores:")
    print(sorted(fitness_scores, reverse=True)[:5])

def debug_constraints(team):
    position_counts = {pos: 0 for pos in position_constraints}
    for player in team:
        position_counts[player['position']] += 1
    print("Position Counts:", position_counts)
    print("Satisfies Constraints:", satisfies_constraints(team))

def debug_weights_evolution(population):
    print("Agent Weights Over Generations:")
    for i, agent_weights in enumerate(population[:5]):  # Check top 5 agents
        print(f"Agent {i + 1}: {agent_weights}")

def save_debug_teams_to_excel(teams, file_name="debug_teams.xlsx"):
    team_data = []
    for i, team in enumerate(teams):
        for player in team:
            team_data.append({"Agent": i + 1, "Player": player['playerName'], "Position": player['position'], "Total Points": player['totalPoints'], "ADP": player['adp']})
    df = pd.DataFrame(team_data)
    df.to_excel(file_name, index=False)
    print(f"Teams saved to {file_name}")

def calculate_population_diversity(population):
    diversity = len(set(tuple(agent.items()) for agent in population))
    print(f"Population Diversity: {diversity}")

# Step 2: Load Player Data
def load_player_data(file_path):
    df = pd.read_excel(file_path)
    players = df.to_dict(orient="records")  # Convert to list of dictionaries for easier processing
    return players

# Save the final team to an Excel file
def save_team_to_excel(team, file_name="final_team.xlsx"):
    df = pd.DataFrame(team)
    df.to_excel(file_name, index=False)
    print(f"Final team saved to {file_name}")

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
# Step 5: Team Selection with ADP and Position Constraints
# Step 5: Team Selection with ADP and Position Constraints
# Step 5: Team Selection with ADP and Position Constraints
def select_team(agent_weights, players, pick_order):
    team = []
    position_counts = {pos: 0 for pos in position_constraints}
    selected_player_ids = set()  # Track selected players to avoid duplicates

    for i, round_pick in enumerate(pick_order):
        # For the first pick, there are no ADP constraints
        if i == 0:
            filtered_players = [
                p for p in players if p["playerId"] not in selected_player_ids
            ]
        else:
            # Apply ADP constraint for subsequent picks
            filtered_players = [
                p for p in players 
                if p["adp"] >= round_pick and p["playerId"] not in selected_player_ids
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
                selected_player_ids.add(player["playerId"])  # Mark as selected
                break  # Proceed to the next pick

    # Validate the team satisfies all constraints
    if satisfies_constraints(team):
        return team
    return []



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

# Step 8: Run Genetic Algorithm
def genetic_algorithm(players, pick_order, pop_size=50, generations=200):
    attribute_keys = [
        "height", "weight", "age", "injuries", "passingYards", "attempts", "completions", 
        "interceptions", "sacks", "passingTDs", "passing2Pts", "receptions", "targets", 
        "receivingYards", "receivingTDs", "receiving2Pts", "rushingYards", "carries", 
        "rushingTDs", "rushing2Pts", "fumbles", "avgArticleScore"
    ]
    population = generate_initial_population(pop_size, attribute_keys)

    stagnation_threshold = 5
    mutation_rate = 0.1

    for generation in range(generations):
        fitness_scores = [
            calculate_team_score(select_team(agent, players, pick_order))
            for agent in population
        ]
        sorted_population = sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)

        # Check Convergence
        unique_fitness, unique_agents = len(set(fitness_scores)), len(set(tuple(agent.items()) for agent in population))
        if unique_fitness <= 1 or unique_agents <= 1:
            print(f"Population has converged in Generation {generation + 1}! Injecting diversity...")
            population = inject_random_agents(population, pop_size, attribute_keys)

        # Adaptive Mutation Rate
        if len(set(fitness_scores[-stagnation_threshold:])) == 1:
            mutation_rate = 0.3  # Increase mutation rate
        else:
            mutation_rate = 0.1

        # Debugging Outputs
        if generation % 10 == 0:
            print(f"--- Generation {generation + 1} ---")
            debug_agent_scores(sorted_population[0][1], players)
            debug_selected_team(sorted_population[0][1], players, pick_order)
            debug_population_diversity(population)
            debug_fitness_scores(fitness_scores)

        population = [x[1] for x in sorted_population[:pop_size // 2]]

        while len(population) < pop_size:
            if random.random() < 0.1:
                random_agent = {key: random.uniform(0, 1) for key in attribute_keys}
                population.append(random_agent)
            else:
                parent1, parent2 = random.choices([x[1] for x in sorted_population[:pop_size // 2]], k=2)
                child = crossover(parent1, parent2)
                mutate(child, mutation_rate)
                population.append(child)

    best_agent = population[0]
    best_team = select_team(best_agent, players, pick_order)
    save_team_to_excel(best_team, "final_team_with_adp.xlsx")
    return best_team, best_agent

# Run the Process
file_path = "/Users/7one/Documents/NortheasternDengfeng/Study in NEU/1 - Master Course/CS5100 Foundations Artificial Intelligence/FinalProject/table/demo180.xlsx"
players = load_player_data(file_path)
pick_order = [1, 24, 25, 48, 49, 72, 73, 96, 97, 120, 121, 144, 145, 168]  # Custom pick order
best_team, best_agent = genetic_algorithm(players, pick_order, pop_size=50, generations=200)
print("Best Agent Weights:", best_agent)
