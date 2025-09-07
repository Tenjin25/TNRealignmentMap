import os
import pandas as pd

# Directory containing election data CSVs
data_dir = os.path.join(os.path.dirname(__file__), 'Election_Data')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

# Read and concatenate all CSVs
df_list = []
for file in csv_files:
    path = os.path.join(data_dir, file)
    try:
        df = pd.read_csv(path, dtype=str, low_memory=False)
        df['source_file'] = file  # Track source
        df_list.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Find common columns
if df_list:
    # Get intersection of columns
    common_cols = set(df_list[0].columns)
    for df in df_list[1:]:
        common_cols &= set(df.columns)
    common_cols = list(common_cols)
    # Merge on common columns
    merged = pd.concat([df[common_cols] for df in df_list], ignore_index=True)
    merged.to_csv('merged_election_data.csv', index=False)
    print(f"Merged {len(csv_files)} files into merged_election_data.csv with {len(merged)} rows.")
else:
    print("No CSV files found or all failed to read.")
