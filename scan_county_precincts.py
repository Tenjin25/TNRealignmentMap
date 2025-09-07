import pandas as pd
import glob

csv_files = glob.glob('Election_Data/standardized/*_standardized.csv')

for csv in sorted(csv_files):
    print(f"\n--- {csv} ---")
    try:
        df = pd.read_csv(csv, dtype=str)
        df.columns = df.columns.str.strip()
        # Show unique COUNTY and PRECINCT values (stripped and upper)
        if 'COUNTY' in df.columns and 'PRECINCT' in df.columns:
            counties = df['COUNTY'].astype(str).str.strip().str.upper().unique()
            precincts = df['PRECINCT'].astype(str).str.strip().str.upper().unique()
            print(f"COUNTY sample: {list(counties)[:10]}")
            print(f"PRECINCT sample: {list(precincts)[:10]}")
            print(f"COUNTY count: {len(counties)} | PRECINCT count: {len(precincts)}")
        else:
            print("COUNTY or PRECINCT column missing!")
    except Exception as e:
        print(f"Error reading {csv}: {e}")
