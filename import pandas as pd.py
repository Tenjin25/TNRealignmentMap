import pandas as pd
import os
import glob
import json

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')
pattern = os.path.join(STANDARDIZED_DIR, '*_enhanced.csv')
files = [f for f in glob.glob(pattern) if any(y in f for y in ['2008', '2010', '2012'])]

combined = {}

for f in files:
    year = os.path.basename(f)[:4]
    df = pd.read_csv(f, dtype=str)
    # Ensure numeric fields are correct
    for col in ['VOTES', 'dem_votes', 'rep_votes', 'other_votes', 'total_votes', 'margin', 'margin_pct']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if year not in combined:
        combined[year] = {}
    for contest, group in df.groupby('OFFICENAME'):
        contest_key = contest.strip().replace(' ', '_').upper()
        combined[year][contest_key] = []
        for _, row in group.iterrows():
            combined[year][contest_key].append(row.dropna().to_dict())

output_path = os.path.join(STANDARDIZED_DIR, 'tn_legacy_comprehensive.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print(f"Combined JSON written to {output_path}")