import sys
import os
import logging
from datetime import datetime

# add project folder to path
sys.path.append(os.getcwd())

from src.extract import extract_data
from src.clean import clean_data
from src.load import load_to_postgres

# setting up logs to track what happens
# this creates a file in logs/pipeline.log
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    print("starting the etl pipeline project")
    logging.info("pipeline started running")

    try:
        # phase 1 extract
        logging.info("starting phase 1 extraction")
        df_raw = extract_data()
        
        if df_raw is None:
            logging.error("extraction failed no data found")
            return

        # phase 2 clean
        logging.info(f"starting phase 2 cleaning with {len(df_raw)} rows")
        df_clean = clean_data(df_raw)

        # phase 3 load
        logging.info(f"starting phase 3 loading with {len(df_clean)} rows")
        load_to_postgres(df_clean)

        logging.info("pipeline finished successfully")
        print("finished everything successfully check logs/pipeline.log if you want details")

    except Exception as e:
        logging.error(f"pipeline crashed {e}")
        print(f"pipeline crashed because {e}")

if __name__ == "__main__":
    run_pipeline()