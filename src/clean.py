import pandas as pd
import sys
import os

# adding project folder to path so i can import extract
sys.path.append(os.getcwd())
from src.extract import extract_data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    fixes column names and makes sure data types are correct
    """
    print("starting to clean the data")

    # changing arabic column names to english
    column_mapping = {
        'السنة': 'year',
        'الربع': 'quarter',
        'الدولة': 'country',
        'قيمة - ريال': 'import_value',
        'الوزن الصافي بالكيلو': 'weight_kg',
        'رمز التعرفة 4 خانات': 'commodity_code'
    }
    
    # rename the columns
    df.rename(columns=column_mapping, inplace=True)

    # fix the quarter column so it just says Q1 instead of Q1-2025
    if 'quarter' in df.columns:
        df['quarter'] = df['quarter'].astype(str).apply(lambda x: x.split('-')[0] if '-' in x else x)

    # make sure these columns are actually numbers
    numeric_cols = ['import_value', 'weight_kg', 'year']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # remove extra spaces from country names
    if 'country' in df.columns:
        df['country'] = df['country'].astype(str).str.strip()

    # remove duplicate rows if there are any
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    if len(df) < initial_count:
        print(f"removed {initial_count - len(df)} duplicate rows")

    print("finished cleaning the data")
    return df

if __name__ == "__main__":
    # testing if this works
    print("testing clean phase")
    
    # run extract first
    df_raw = extract_data()
    
    if df_raw is not None:
        # then run clean
        df_cleaned = clean_data(df_raw)
        
        # show me what it looks like
        print("\n--- sample of cleaned data ---")
        print(df_cleaned.head())
        print("\n--- data info ---")
        print(df_cleaned.info())
    else:
        print("cant clean because extraction failed")