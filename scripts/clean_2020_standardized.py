
import pandas as pd
import os
import glob

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')

# Only process modern years (2014, 2016, 2018, 2020, 2022, 2024)
pattern = os.path.join(STANDARDIZED_DIR, '*_standardized.csv')
modern_years = ['2014', '2016', '2018', '2020', '2022', '2024']
files = [f for f in glob.glob(pattern) if any(y in os.path.basename(f) for y in modern_years)]

def process_file(input_path):
    base_name = os.path.basename(input_path)
    output_path = os.path.join(STANDARDIZED_DIR, base_name.replace('.csv', '_long.csv'))
    df = pd.read_csv(input_path, dtype=str, skipinitialspace=True)
    df.columns = [c.strip().replace(' ', '_').upper() for c in df.columns]
    candidate_cols = []
    for i in range(1, 21):
        candidate_cols.append({
            'COLHDG': f'COL{i}HDG',
            'RNAME': f'RNAME{i}',
            'PARTY': f'PARTY{i}',
            'PVTALLY': f'PVTALLY{i}'
        })
    records = []
    for idx, row in df.iterrows():
        base = {k: row[k] for k in df.columns if not any(k.startswith(x) for x in ['COL', 'RNAME', 'PARTY', 'PVTALLY'])}
        for cand in candidate_cols:
            def safe_strip(val):
                if pd.isna(val):
                    return ''
                return str(val).strip()
            name = safe_strip(row.get(cand['RNAME'], ''))
            party = safe_strip(row.get(cand['PARTY'], ''))
            tally = safe_strip(row.get(cand['PVTALLY'], ''))
            if name and tally:
                try:
                    tally_int = int(float(tally))
                except Exception:
                    tally_int = None
                records.append({
                    **base,
                    'CANDIDATE': name,
                    'PARTY': party,
                    'VOTES': tally_int
                })
    long_df = pd.DataFrame(records)
    if long_df.empty or not set(['CANDIDATE', 'VOTES']).issubset(long_df.columns):
        print(f"Warning: No candidate data found in {input_path}. Skipping output.")
        return
    long_df = long_df.dropna(subset=['CANDIDATE', 'VOTES'])
    long_df.to_csv(output_path, index=False)
    print(f"Wrote long-form results to {output_path}")

if __name__ == '__main__':
    for f in files:
        print(f"Processing {f}...")
        process_file(f)
    print("All files processed.")
