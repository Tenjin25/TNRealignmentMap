import pandas as pd
import glob

# List of all standardized election CSVs
csv_files = glob.glob('Election_Data/standardized/*_standardized.csv')

for csv in sorted(csv_files):
    try:
        df = pd.read_csv(csv, dtype=str, nrows=1)
        # Strip whitespace from all column names
        df.columns = df.columns.str.strip()
        print(f"{csv} columns:")
        print(list(df.columns))
        print("Sample row:")
        print(df.iloc[0].to_dict())
        print("-"*60)
    except Exception as e:
        print(f"Error reading {csv}: {e}")
        print("-"*60)
