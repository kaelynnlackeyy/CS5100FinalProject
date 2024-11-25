import datetime
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey, Text, Float, Date, insert
import pandas as pd
from pandasql import sqldf
import re
from datetime import datetime

user = 'admin'
password = 'fillerpassword'
host = 'fantasy-football-ai.c180k46m8sh9.us-east-1.rds.amazonaws.com'
database_name = 'fantasyfootballproject'

'''
Function: Creates a database on the server
Parameters: None
Returns: None
'''
def create_database():
    # Connects first to server to create a database if it doesn't exist
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}")

    # Closes connection after use
    with engine.connect() as con:
        con.execute(text("CREATE DATABASE IF NOT EXISTS fantasyfootballproject"))


'''
Function: Creates tables in the database and in the metadata dictionary
Parameters: None
Returns: None
'''
def database_layout():
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database_name}")
    metadata = MetaData()
    positions = Table('positions', metadata, Column('posid', Integer, primary_key = True, autoincrement = True), Column('positionName', String(50)))
    players = Table('players', metadata, Column('pid', Integer, primary_key = True, autoincrement = True), Column('playerName', String(50)), Column('position', Integer, ForeignKey('positions.posid')))
    fumbles = Table('fumbles', metadata, Column('fid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('fumbles', Integer), Column('year', Integer))
    passing = Table('passing', metadata, Column('psid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('passingYards', Integer), Column('attempts', Integer), Column('completions', Integer), Column('interceptions', Integer), Column('sacks', Integer), Column('passingTDs', Integer), Column('passing2Pts', Integer), Column('year', Integer))
    rushing = Table('rushing', metadata, Column('rsid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('rushingYards', Integer), Column('carries', Integer), Column('rushingTDs', Integer), Column('rushing2Pts', Integer), Column('year', Integer))
    receiving = Table('receiving', metadata, Column('recsid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('receptions', Integer), Column('targets', Integer), Column('receivingYards', Integer), Column('receivingTDs', Integer), Column('receiving2Pts', Integer), Column('year', Integer))
    articles = Table('articles', metadata, Column('aid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('articleText', Text(length = 16777215)), Column('articleScore', Integer), Column('date', Date))
    playerRankingByYear = Table('playerRankingByYear', metadata, Column('prid', Integer, primary_key = True, autoincrement = True), Column('playerId', Integer, ForeignKey('players.pid')), Column('height', Integer), Column('weight', Integer), Column('age', Integer), Column('injuries', Integer), Column('adp', Float), Column('totalPoints', Integer), Column('year', Integer))
    metadata.create_all(engine)
    data = [{'positionName': 'QB'}, {'positionName': 'WR'}, {'positionName': 'RB'}, {'positionName': 'TE'}]
    
    with engine.connect() as conn:
        stmt = insert(positions).values(data)
        conn.execute(stmt)
        conn.commit()

        fill_database(players, fumbles, passing, rushing, receiving, articles, playerRankingByYear)


'''
Function: Takes in data from the CSV file, manipulates it, and loads it into the database.
Parameters: Takes in tables for the data to be loaded into
Returns: None
'''
def fill_database(players, fumbles, passing, rushing, receiving, articles, playerRankingByYear):
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database_name}")

    with engine.connect() as conn:
        # Retrieve positions table for foreign keys
        result = conn.execute(text('SELECT * FROM positions'))
        positions_df = pd.DataFrame(result.fetchall(), columns = ['posid', 'positions'])

        # Load data from csv
        player_stats_df = pd.read_csv("player_stats_season.csv")
        viable_positions = set(('QB', 'WR', 'TE', 'RB'))
        
        # Drop unnecessary data
        player_stats_df.drop(['player_name', 'position', 'headshot_url', 'games', 'recent_team', 'sack_yards', 
                            'sack_fumbles_lost', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 'passing_epa', 'pacr', 
                            'dakota', 'rushing_fumbles_lost', 'rushing_first_downs', 'rushing_epa', 'receiving_fumbles_lost', 'receiving_air_yards', 
                            'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa', 'racr', 'target_share', 'air_yards_share', 'wopr', 'fantasy_points'], axis = 1, inplace = True)
        
        player_stats_df.drop(player_stats_df[~player_stats_df['position_group'].isin(viable_positions)].index, inplace = True)
        player_stats_df.drop(player_stats_df[player_stats_df.season < 2017].index, inplace = True)
        player_stats_df.drop(player_stats_df[player_stats_df.season_type != 'REG'].index, inplace = True)
       
        # Create the players table and load it in
        player_stats_df = sqldf("SELECT player_stats_df.*, posid FROM player_stats_df INNER JOIN positions_df ON (player_stats_df.position_group = positions_df.positions)")
        players_df = sqldf("SELECT player_display_name as playerName, posid AS position FROM player_stats_df GROUP BY player_id").to_dict(orient = 'records')
        
        player_stmt = insert(players).values(players_df)
        conn.execute(player_stmt)
        conn.commit()
        
        # Retrieve the players table for foreign keys
        result = conn.execute(text('SELECT * FROM players'))
        players_df = pd.DataFrame(result.fetchall(), columns = ['pid', 'playerName', 'position'])
        
        # Set up other tables in database
        fumble_stats_df = sqldf("SELECT pid as playerId, (sack_fumbles + rushing_fumbles + receiving_fumbles) as fumbles, season as year FROM player_stats_df INNER JOIN players_df ON (player_stats_df.player_display_name = players_df.playerName) GROUP BY player_id, season")
        passing_stats_df = sqldf('SELECT pid as playerId, passing_yards as passingYards, attempts, completions, interceptions, sacks, passing_tds as passingTDs, passing_2pt_conversions as passing2Pts, season as year FROM player_stats_df INNER JOIN players_df ON (player_stats_df.player_display_name = players_df.playerName) GROUP BY player_id, season')
        rushing_stats_df = sqldf('SELECT pid as playerId, rushing_yards as rushingYards, carries, rushing_tds as rushingTDs, rushing_2pt_conversions as rushing2Pts, season as year FROM player_stats_df INNER JOIN players_df ON (player_stats_df.player_display_name = players_df.playerName) GROUP BY player_id, season')
        receiving_stats_df = sqldf('SELECT pid as playerId, receptions, targets, receiving_yards as receivingYards, receiving_tds as receivingTDs, receiving_2pt_conversions as receiving2Pts, season as year FROM player_stats_df INNER JOIN players_df ON (player_stats_df.player_display_name = players_df.playerName) GROUP BY player_id, season')
        player_data_df = personal_player_stats(player_stats_df, players_df)
        articles_df = article_df_creator(players_df)

        # Prepare data to be loaded
        fumble_stats_df = fumble_stats_df.to_dict(orient = 'records')
        passing_stats_df = passing_stats_df.to_dict(orient = 'records')
        rushing_stats_df = rushing_stats_df.to_dict(orient = 'records')
        receiving_stats_df = receiving_stats_df.to_dict(orient = 'records')
        player_data_df = player_data_df.to_dict(orient = 'records')
        articles_df = articles_df.to_dict(orient = 'records')

        # Load data
        fumbles_stmt = insert(fumbles).values(fumble_stats_df)
        passing_stmt = insert(passing).values(passing_stats_df)
        rushing_stmt = insert(rushing).values(rushing_stats_df)
        receiving_stmt = insert(receiving).values(receiving_stats_df)
        playerRankingByYear_stmt = insert(playerRankingByYear).values(player_data_df)
        articles_stmt = insert(articles).values(articles_df)

        conn.execute(fumbles_stmt)
        conn.execute(passing_stmt)
        conn.execute(rushing_stmt)
        conn.execute(receiving_stmt)
        conn.execute(playerRankingByYear_stmt)
        conn.execute(articles_stmt)
        conn.commit()

'''
Function: Creates a dataframe that contains all personal stats about players
Parameters: Takes in 2 dataframes to help build the final dataframe
Return: A dataframe containing personal stats about players 
'''
def personal_player_stats(player_stats_df, players_df):
    # Create a dataframe that contains players' personal data
    player_data_df = pd.read_csv('yearly_player_data_includes_player_info.csv')
    adp_values = pd.read_csv('adp_merged_7_17.csv')
    player_data_df = sqldf('SELECT pid AS playerId, height, weight, age, injuries, adp, player_stats_df.fantasy_points_ppr as totalPoints, player_data_df.season AS year FROM player_data_df LEFT JOIN adp_values ON(player_data_df.player_name = adp_values.name AND player_data_df.season = adp_values.Year) INNER JOIN players_df ON (players_df.playerName = player_data_df.player_name) INNER JOIN player_stats_df ON (player_data_df.player_name = player_stats_df.player_display_name AND player_data_df.season = player_stats_df.season)')

    player_data_df.fillna({'adp': -1.0}, inplace=True) # Replace NULL adp with -1.0

    return player_data_df

'''
Function: Loads a dataframe with the articles, scores, dates, and the player IDs
Parameters: Takes in the dataframe for players and their playerID.
Return: A dataframe containing the players' ID and their associated articles.
'''
def article_df_creator(players_df):
    # Extracts the date from the dataframe string.
    def extract_date(text):
        date_pattern = r"\b\d{1,2}/\d{1,2}/\d{4}\b"
        extracted_date = re.search(date_pattern, text).group()
        date_object = datetime.strptime(extracted_date, "%m/%d/%Y")

        return date_object.strftime("%Y-%m-%d")

    # Extracts a player's name from the dataframe string.
    def extract_name(text):
        text_split = text.split(" - ")
        return text_split[0]
    
    articles_df = pd.read_csv('player_news_table_with_labels.csv')
    articles_df['player_news_date'] = articles_df['player_news_date'].apply(extract_date)
    articles_df['player_name'] = articles_df['player_name'].apply(extract_name)
    articles_w_players = sqldf('SELECT pid AS playerId, player_news AS articleText, label AS articleScore, player_news_date AS date FROM articles_df INNER JOIN players_df ON (articles_df.player_name = players_df.playerName)')
    return articles_w_players
    

def main():
    create_database()
    database_layout()

if __name__ == '__main__':
    main()