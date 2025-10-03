import pandas as pd
import os
import glob

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')
pattern = os.path.join(STANDARDIZED_DIR, '*_standardized_long.csv')
files = [f for f in glob.glob(pattern) if any(y in f for y in ['2008', '2010', '2012'])]

# 15 standard columns for NC/TN map compatibility
COLUMNS = [
    'year', 'county', 'county_fips', 'precinct', 'vtd_id',
    'office', 'district', 'candidate', 'party', 'votes',
    'total_votes', 'winner', 'margin', 'turnout', 'swing'
]

def process_file(input_path):
    base_name = os.path.basename(input_path)
    year = base_name[:4]
    output_path = os.path.join(STANDARDIZED_DIR, base_name.replace('_long.csv', '_final.csv'))
    df = pd.read_csv(input_path, dtype=str)
    # Try to map legacy columns to standard ones
    out = pd.DataFrame()
    out['year'] = year
    out['county'] = df['COUNTY'] if 'COUNTY' in df else ''
    out['county_fips'] = ''  # Can be filled in later with a crosswalk
    out['precinct'] = df['PRECINCT'] if 'PRECINCT' in df else ''
    out['vtd_id'] = ''  # Can be filled in later if available
    out['office'] = df['OFFICENAME'] if 'OFFICENAME' in df else ''
    out['district'] = df['DISTRICT'] if 'DISTRICT' in df else ''
    out['candidate'] = df['CANDIDATE'] if 'CANDIDATE' in df else ''
    out['party'] = df['PARTY'] if 'PARTY' in df else ''
    out['votes'] = df['VOTES'] if 'VOTES' in df else ''
    out['total_votes'] = ''  # Can be calculated later
    out['winner'] = ''      # Can be calculated later
    out['margin'] = ''      # Can be calculated later
    out['turnout'] = ''     # Can be calculated later
    out['swing'] = ''       # Can be calculated later
    out = out[COLUMNS]
    out.to_csv(output_path, index=False)
    print(f"Wrote standardized file to {output_path}")

if __name__ == '__main__':
    for f in files:
        print(f"Processing {f}...")
        process_file(f)
    print("All legacy files standardized.")
