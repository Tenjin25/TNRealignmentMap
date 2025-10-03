import pandas as pd
import os
import glob
import re

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')
pattern = os.path.join(STANDARDIZED_DIR, '*_standardized.csv')
files = glob.glob(pattern)

# Process all legacy files (2004, 2006, 2008, 2010, 2012), including office-specific files
legacy_years = ['2004', '2006', '2008', '2010', '2012']
legacy_files = [f for f in files if any(y in os.path.basename(f) for y in legacy_years)]

def extract_name_party(bname):
    if pd.isna(bname) or not str(bname).strip():
        return '', ''
    # Try to split on last ' - (' for party in parens, else just name
    m = re.match(r"(.+?)\s*-\s*\(([^)]+)\)", str(bname).strip())
    if m:
        return m.group(1).strip('. '), m.group(2).strip()
    # Try to split on last ' - '
    parts = str(bname).rsplit(' - ', 1)
    if len(parts) == 2:
        return parts[0].strip('. '), parts[1].strip()
    return str(bname).strip('. '), ''

def process_file(input_path):
    base_name = os.path.basename(input_path)
    output_path = os.path.join(STANDARDIZED_DIR, base_name.replace('.csv', '_long.csv'))
    df = pd.read_csv(input_path, dtype=str, skipinitialspace=True)
    df.columns = [c.strip().replace(' ', '_').upper() for c in df.columns]
    # Find candidate columns
    candidate_cols = []
    for i in range(1, 11):
        candidate_cols.append({
            'BNAME': f'BNAME{i}',
            'TALLY': f'TALLY{i}'
        })
    records = []
    for idx, row in df.iterrows():
        base = {k: row[k] for k in df.columns if not any(k.startswith(x) for x in ['COL', 'BNAME', 'TALLY'])}
        for cand in candidate_cols:
            bname = row.get(cand['BNAME'], '')
            tally = row.get(cand['TALLY'], '')
            name, party = extract_name_party(bname)
            try:
                votes = int(float(tally)) if tally and not pd.isna(tally) else None
            except Exception:
                votes = None
            if name and votes is not None:
                records.append({
                    **base,
                    'CANDIDATE': name,
                    'PARTY': party,
                    'VOTES': votes
                })
    long_df = pd.DataFrame(records)
    if long_df.empty or not set(['CANDIDATE', 'VOTES']).issubset(long_df.columns):
        print(f"Warning: No candidate data found in {input_path}. Skipping output.")
        return
    long_df.to_csv(output_path, index=False)
    print(f"Wrote long-form results to {output_path}")

if __name__ == '__main__':
    for f in legacy_files:
        print(f"Processing {f}...")
        process_file(f)
    print("All legacy files processed.")
