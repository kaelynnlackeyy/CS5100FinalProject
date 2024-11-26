from sqlalchemy import create_engine, text
import pandas as pd

# Login credentials for db
user = 'admin'
password = 'fillerpassword'
host = 'fantasy-football-ai.c180k46m8sh9.us-east-1.rds.amazonaws.com'
database_name = 'fantasyfootballproject'

def data_grabber(year):
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}")

    with engine.connect() as conn:
        result = conn.execute(text(f"WITH articles (playerId, avgArticleScore, season) AS (SELECT playerId, AVG(articleScore) as avgArticleScore, YEAR(date) AS season FROM fantasyfootballproject.articles GROUP BY playerId, season) SELECT playerName, pid, posid AS position, passing.year as prevSeason, height, weight, age, injuries, adp, totalPoints, passingYards, attempts, completions, interceptions, sacks, passingTDs, passing2Pts, receptions, targets, receivingYards, receivingTDs, receiving2Pts, rushingYards, carries, rushingTDs, rushing2Pts, fumbles, avgArticleScore FROM fantasyfootballproject.players p INNER JOIN fantasyfootballproject.positions pos ON (p.position = pos.posid) INNER JOIN fantasyfootballproject.passing passing ON (p.pid = passing.playerId) INNER JOIN fantasyfootballproject.receiving rec ON (passing.playerId = rec.playerId AND passing.year = rec.year) INNER JOIN fantasyfootballproject.rushing rush ON (rec.playerId = rush.playerId AND rec.year = rush.year) INNER JOIN fantasyfootballproject.fumbles f ON (f.playerId = rush.playerId AND f.year = rush.year) INNER JOIN fantasyfootballproject.playerRankingByYear prby ON (passing.playerId = prby.playerId AND passing.year = prby.year - 1) LEFT JOIN articles a ON (a.playerId = prby.playerId AND passing.year = a.season - 1) WHERE passing.year = {year - 1}"))
        data_df = pd.DataFrame(result.fetchall(), columns = ['playerName', 'pid', 'position', 'prevSeason', 'height', 'weight', 'age', 'injuries', 'adp', 'totalPoints', 'passingYards', 'attempts', 'completions', 'interceptions', 'sacks', 'passingTDs', 'passing2Pts', 'receptions', 'targets', 'receivingYards', 'receivingTDs', 'receiving2Pts', 'rushingYards', 'carries', 'rushingTDs', 'rushing2Pts', 'fumbles', 'avgArticleScore'])
        data_df.fillna({'avgArticleScore': 0.51746529}, inplace=True)
        data_df.to_excel(f"stats_for_{year}.xlsx")

def main():
    data_grabber(2023)

if __name__ == '__main__':
    main()