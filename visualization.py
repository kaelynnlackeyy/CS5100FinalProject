

import matplotlib.pyplot as plt
from generic_codevStandard import genetic_algorithm,load_player_data,select_team,calculate_team_score,calculate_agent_score
import pandas as pd
import numpy as np
import random
# run genetic algorithm,save each best team to a separate file.

# x axis: either generation or optimal ADP from each run of the genetic algorithm
# y axis: avg article score weight
# agent_weights['avgArticleScore']

season=int(input('Enter the season you wish to draft for: '))
file_path=f"stats_for_{season}.xlsx"
players=load_player_data(file_path)

pick_order=random.sample(range(1,201),14)
pop_size=random.randint(20,100)
generations=[]
avg_article_scores=[]
avg_adp_scores=[]
avg_agent_scores = []
avg_team_scores = []


for run in range(1):
    population=None
    for generation in range(200):
        best_team,best_agent=genetic_algorithm(players,pick_order,pop_size=pop_size,generations=1)
        avg_article_score_weight=best_agent['avgArticleScore']
        best_team=select_team(best_agent,players,pick_order)
        avg_adp_score=np.mean([player['adp'] for player in best_team if 'adp' in player])
        avg_agent_score = np.mean([calculate_agent_score(player, best_agent) for player in best_team])
        avg_article_scores.append(avg_article_score_weight)
        avg_agent_scores.append(avg_agent_score)
        avg_adp_scores.append(avg_adp_score)
        team_score=calculate_team_score(best_team)
        avg_team_scores.append(team_score)
    generations.append(generation + 1)
    file_name=f"best_team_run_{run+1}.xlsx"
    df=pd.DataFrame(best_team)
    df.to_excel(file_name,index=False)

figure,axis=plt.subplots()
axis.scatter(generations,avg_article_scores,c='#008080',alpha=0.5)
axis.set_xlabel('generation')
axis.set_ylabel('average article weight')
plt.title('Avg Article Score Weight across generations')
plt.savefig('generation.png')
plt.show()

figure,axis=plt.subplots()
axis.scatter(avg_article_scores,avg_adp_scores,c='#008080',alpha=0.5)
axis.set_xlabel('avg article score weight')
axis.set_ylabel('ADP score')
plt.title('ADP Score vs Average Article Score Weight')
plt.savefig('aasvsadp.png')
plt.show()

figure,axis=plt.subplots()
axis.scatter(avg_team_scores,avg_article_scores,c='#008080',alpha=0.5)
axis.set_xlabel('average team score')
axis.set_ylabel('avg article score weight')
plt.title('Avg Article Score Weight vs Average Team Score')
plt.savefig('aatsvaas.png')
plt.show()

figure,axis=plt.subplots()
axis.scatter(avg_article_scores,avg_team_scores,c='#008080',alpha=0.5)
axis.set_xlabel('average article weight')
axis.set_ylabel('average team score')
plt.title('Avg Article Score Weight vs Average Team Score')
plt.savefig('averageteamflipped.png')
plt.show()

figure,axis=plt.subplots()
axis.scatter(avg_agent_scores,avg_article_scores,c='#008080',alpha=0.5)
axis.set_xlabel('average agent score')
axis.set_ylabel('avg article score weight')
plt.title('Avg Article Score Weight vs Average Agent Score')
plt.savefig('aasvaas.png')
plt.show()

figure,axis=plt.subplots()
axis.scatter(avg_article_scores,avg_agent_scores,c='#008080',alpha=0.5)
axis.set_xlabel('avg article score weight')
axis.set_ylabel('average agent score')
plt.title('Avg Article Score Weight vs Average Agent Score')
plt.savefig('averageagentflipped.png')
plt.show()

