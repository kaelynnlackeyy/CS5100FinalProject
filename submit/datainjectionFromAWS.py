import pandas as pd
from sqlalchemy import create_engine
import os  # To handle file paths dynamically

# Database connection details
user = 'admin'
password = 'fillerpassword'
host = 'fantasy-football-ai.c180k46m8sh9.us-east-1.rds.amazonaws.com'
database_name = 'fantasyfootballproject'

# Function to generate SQL query for a specific year
def generate_query(year):
    return f"""
    WITH articles (playerId, avgArticleScore, season) AS (SELECT playerId, AVG(articleScore) as avgArticleScore, YEAR(date) 
    AS season FROM fantasyfootballproject.articles GROUP BY playerId, season) 
    
    SELECT playerName, pid, posid AS position, passing.year as prevSeason, height, weight, age, injuries, adp, totalPoints, 
    passingYards, attempts, completions, interceptions, sacks, passingTDs, passing2Pts, receptions, targets, receivingYards, 
    receivingTDs, receiving2Pts, rushingYards, carries, rushingTDs, rushing2Pts, fumbles, avgArticleScore 
    FROM fantasyfootballproject.players p 
    INNER JOIN fantasyfootballproject.positions pos ON (p.position = pos.posid) 
    INNER JOIN fantasyfootballproject.passing passing ON (p.pid = passing.playerId) 
    INNER JOIN fantasyfootballproject.receiving rec ON (passing.playerId = rec.playerId AND passing.year = rec.year) 
    INNER JOIN fantasyfootballproject.rushing rush ON (rec.playerId = rush.playerId AND rec.year = rush.year) 
    INNER JOIN fantasyfootballproject.fumbles f ON (f.playerId = rush.playerId AND f.year = rush.year) 
    INNER JOIN fantasyfootballproject.playerRankingByYear prby ON (passing.playerId = prby.playerId AND passing.year = prby.year - 1)
    LEFT JOIN articles a ON (a.playerId = prby.playerId AND passing.year = a.season - 1) WHERE passing.year = {year - 1};
    """

# Connect to the database and fetch data
def fetch_data_from_aws(user, password, host, database_name, query):
    try:
        # Create the connection engine
        connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database_name}"
        engine = create_engine(connection_string)

        # Fetch data into a pandas DataFrame
        print(f"Fetching data for query: {query[:100]}...")
        df = pd.read_sql(query, engine)
        print("Data fetched successfully!")

        return df
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Save the DataFrame to a CSV file
def save_to_csv(df, file_name):
    try:
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, file_name)  # Construct the full path
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_name} successfully!")
    except Exception as e:
        print("Error saving to CSV:", e)

# Main Execution
if __name__ == "__main__":
    # Define the range of years
    start_year = 2017
    end_year = 2022
    combined_data = []  # For appending data across years

    for year in range(start_year, end_year + 1):
        # Generate the SQL query for the specific year
        query = generate_query(year)

        # Fetch data for the specific year
        df = fetch_data_from_aws(user, password, host, database_name, query)

        if df is not None:
            # Handle missing values for `avgArticleScore`
            df.fillna({'avgArticleScore': 0.51746529}, inplace=True)  # Replace with your default value
            print(f"Missing values handled successfully for year {year}.")

            # Save the processed data to a CSV file
            csv_file_name = f"player_data_{year}.csv"  # Save per year
            save_to_csv(df, csv_file_name)

            # Append to combined dataset
            df['year'] = year  # Add the year column
            combined_data.append(df)

    # Save combined data to a single CSV file (optional)
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_csv_file = "combined_player_data_2012_2022.csv"
        save_to_csv(combined_df, combined_csv_file)
        print(f"Combined data for all years saved to {combined_csv_file}.")
