import pandas as pd
import os
import glob

# where the raw data is
RAW_DATA_PATH = os.path.join("data", "raw")

def extract_data():
    """
    finds csv and excel files and puts them into one dataframe
    """
    # get all the files from the folder
    all_files = glob.glob(os.path.join(RAW_DATA_PATH, "*"))
    
    if not all_files:
        print(f"cant find any files in {RAW_DATA_PATH}")
        print("please put the csv files in the data/raw folder")
        return None

    df_list = []
    
    for filename in all_files:
        try:
            # check if its a csv file
            if filename.endswith(".csv"):
                # try utf8 encoding first
                try:
                    df = pd.read_csv(filename, encoding='utf-8')
                except UnicodeDecodeError:
                    # if utf8 fails try cp1256 which is common for arabic excel files
                    print(f"utf8 failed for {filename} so trying cp1256")
                    df = pd.read_csv(filename, encoding='cp1256')
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(filename)
            else:
                continue # skip if its not a data file

            # check if the file actually has data
            if not df.empty:
                print(f"loaded file {os.path.basename(filename)} with {len(df)} rows")
                df_list.append(df)
            else:
                print(f"skipping {filename} because its empty")

        except Exception as e:
            print(f"could not load {filename} because {e}")

    # put all the dataframes together
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        print("-" * 30)
        print(f"extracted {len(combined_df)} rows in total")
        return combined_df
    else:
        print("didnt extract any data")
        return None

if __name__ == "__main__":
    extract_data()