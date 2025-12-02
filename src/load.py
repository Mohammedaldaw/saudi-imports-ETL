import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import sys

# setup paths so i can import other files
sys.path.append(os.getcwd())
from src.extract import extract_data
from src.clean import clean_data

# load the password and user from the env file
load_dotenv()

def get_db_engine():
    """
    gets the database connection using credentials from .env
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    
    # create the connection url
    url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url)

def load_to_postgres(df):
    """
    saves the dataframe into the postgres database
    """
    engine = get_db_engine()
    
    print(f"loading {len(df)} rows into postgres now")
    
    try:
        # append means add to existing data and replace means wipe and start over
        df.to_sql('imports_staging', engine, if_exists='append', index=False)
        print("data went into the database correctly")
        
    except Exception as e:
        print(f"something went wrong loading data {e}")

if __name__ == "__main__":
    print("starting the etl pipeline")
    
    # step 1 extract
    df_raw = extract_data()
    
    if df_raw is not None:
        # step 2 clean
        df_clean = clean_data(df_raw)
        
        # step 3 load
        load_to_postgres(df_clean)
        
    print("finished everything")