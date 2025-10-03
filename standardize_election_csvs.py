import os
import pandas as pd

# Map each file to its year and the columns to standardize
ELECTION_FILES = [
    (2008, 'November2008.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2010, 'November2010.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'Precinct Name'}),
    (2012, 'November2012.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2014, '20141104_PrecinctTotals.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2016, 'StateGeneralbyPrecinctNov2016.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2018, 'Nov 2018 General results.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2020, 'Nov2020PrecinctDetail.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2022, '20221108AllbyPrecinct.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'}),
    (2024, '20241105AllbyPrecinct.csv', {'COUNTY': 'COUNTY', 'PRECINCT': 'PRECINCT'})
]

def standardize_election_csvs():
    base = os.path.dirname(__file__)
    data_dir = os.path.join(base, 'Election_Data')
    out_dir = os.path.join(base, 'Election_Data', 'standardized')
    os.makedirs(out_dir, exist_ok=True)
    for year, fname, colmap in ELECTION_FILES:
        in_path = os.path.join(data_dir, fname)
        if not os.path.exists(in_path):
            print(f"Missing: {in_path}")
            continue
        try:
            # Try reading with error_bad_lines/deprecated on pandas >=1.3, use on_bad_lines for newer
            try:
                df = pd.read_csv(in_path, dtype=str, low_memory=False, on_bad_lines='skip')
            except TypeError:
                # For older pandas
                df = pd.read_csv(in_path, dtype=str, low_memory=False, error_bad_lines=False)
            # Clean column names: strip and lower
            df.columns = [c.strip() for c in df.columns]
            colmap_lower = {k: v.strip().lower() for k, v in colmap.items()}
            df_colmap = {c.lower(): c for c in df.columns}
            # Try to find best matches for COUNTY and PRECINCT
            found_cols = {}
            for std_col, orig_col_lower in colmap_lower.items():
                match = None
                for c_lower, c_orig in df_colmap.items():
                    if c_lower == orig_col_lower:
                        match = c_orig
                        break
                if not match:
                    # Try partial match
                    for c_lower, c_orig in df_colmap.items():
                        if orig_col_lower in c_lower:
                            match = c_orig
                            break
                if match:
                    found_cols[std_col] = match
            missing = [std_col for std_col in colmap_lower if std_col not in found_cols]
            if missing:
                print(f"{fname}: Could not find columns for {missing}. Closest columns: {list(df.columns)}. Skipping file.")
                continue
            # Rename found columns to standard names
            df = df.rename(columns={found_cols['COUNTY']: 'COUNTY', found_cols['PRECINCT']: 'PRECINCT'})
            cols = ['COUNTY', 'PRECINCT'] + [c for c in df.columns if c not in ['COUNTY', 'PRECINCT']]
            df = df[cols]
            out_path = os.path.join(out_dir, f'{year}_standardized.csv')
            df.to_csv(out_path, index=False)
            print(f"Standardized {fname} -> {out_path}")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

if __name__ == "__main__":
    standardize_election_csvs()
