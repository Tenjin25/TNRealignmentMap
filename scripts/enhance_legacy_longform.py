import pandas as pd
import os
import glob

def infer_party(party, candidate):
    if pd.isna(party):
        party = ''
    party = str(party).strip().upper()
    candidate = str(candidate).strip().upper() if not pd.isna(candidate) else ''
    if 'DEM' in party or 'DEMOCRAT' in party or 'OBAMA' in candidate or 'BIDEN' in candidate or 'CLINTON' in candidate:
        return 'DEM'
    if 'REP' in party or 'REPUBLICAN' in party or 'TRUMP' in candidate or 'MCCAIN' in candidate or 'ROMNEY' in candidate or 'BUSH' in candidate:
        return 'REP'
    return 'OTHER'

def competitiveness_category(margin_pct):
    # Use NC scale
    if margin_pct is None:
        return '', '', ''
    # Republican
    if margin_pct >= 40:
        return 'Annihilation', 'Republican', '#67000d'
    if 30 <= margin_pct < 40:
        return 'Dominant', 'Republican', '#a50f15'
    if 20 <= margin_pct < 30:
        return 'Stronghold', 'Republican', '#cb181d'
    if 10 <= margin_pct < 20:
        return 'Safe', 'Republican', '#ef3b2c'
    if 5.5 <= margin_pct < 10:
        return 'Likely', 'Republican', '#fb6a4a'
    if 1 <= margin_pct < 5.5:
        return 'Lean', 'Republican', '#fcae91'
    if 0.5 <= margin_pct < 1:
        return 'Tilt', 'Republican', '#fee8c8'
    # Tossup
    if -0.5 < margin_pct < 0.5:
        return 'Tossup', 'Tossup', '#f7f7f7'
    # Democratic
    if -1 < margin_pct <= -0.5:
        return 'Tilt', 'Democratic', '#e1f5fe'
    if -5.5 < margin_pct <= -1:
        return 'Lean', 'Democratic', '#c6dbef'
    if -10 < margin_pct <= -5.5:
        return 'Likely', 'Democratic', '#9ecae1'
    if -20 < margin_pct <= -10:
        return 'Safe', 'Democratic', '#6baed6'
    if -30 < margin_pct <= -20:
        return 'Stronghold', 'Democratic', '#3182bd'
    if -40 < margin_pct <= -30:
        return 'Dominant', 'Democratic', '#08519c'
    if margin_pct <= -40:
        return 'Annihilation', 'Democratic', '#08306b'
    return '', '', ''

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')
pattern = os.path.join(STANDARDIZED_DIR, '*_standardized_long.csv')
files = [f for f in glob.glob(pattern) if any(y in f for y in ['2008', '2010', '2012'])]

def process_file(input_path):
    base_name = os.path.basename(input_path)
    year = base_name[:4]
    output_path = os.path.join(STANDARDIZED_DIR, base_name.replace('_long.csv', '_enhanced.csv'))
    df = pd.read_csv(input_path, dtype=str)
    df['VOTES'] = pd.to_numeric(df['VOTES'], errors='coerce').fillna(0).astype(int)
    df['party_inferred'] = df.apply(lambda r: infer_party(r.get('PARTY', ''), r.get('CANDIDATE', '')), axis=1)
    group_cols = ['COUNTY', 'PRECINCT', 'OFFICENAME']
    results = []
    for keys, group in df.groupby(group_cols):
        county, precinct, contest = keys
        dem_votes = group.loc[group['party_inferred'] == 'DEM', 'VOTES'].sum()
        rep_votes = group.loc[group['party_inferred'] == 'REP', 'VOTES'].sum()
        other_votes = group.loc[group['party_inferred'] == 'OTHER', 'VOTES'].sum()
        total_votes = group['VOTES'].sum()
        margin_raw = rep_votes - dem_votes
        two_party_total = rep_votes + dem_votes
        margin_pct = ((rep_votes - dem_votes) / two_party_total * 100) if two_party_total > 0 else None
        if rep_votes > dem_votes:
            margin = f"R+{abs(margin_raw)}"
            winner = 'REP'
        elif dem_votes > rep_votes:
            margin = f"D+{abs(margin_raw)}"
            winner = 'DEM'
        else:
            margin = 'TIE'
            winner = 'TIE'
        cat, cat_party, cat_color = competitiveness_category(margin_pct)
        for _, row in group.iterrows():
            row_dict = row.to_dict()
            row_dict.update({
                'year': year,
                'total_votes': total_votes,
                'winner': winner,
                'margin': margin,
                'margin_pct': margin_pct if margin_pct is not None else '',
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'competitiveness_category': cat,
                'competitiveness_party': cat_party,
                'competitiveness_color': cat_color
            })
            results.append(row_dict)
    out = pd.DataFrame(results)
    out.to_csv(output_path, index=False)
    print(f"Wrote enhanced file to {output_path}")


# Update file search to include all years (e.g., 2004, 2008, ... 2024, etc.)
pattern = os.path.join(STANDARDIZED_DIR, '*_standardized_long.csv')
files = glob.glob(pattern)

if __name__ == '__main__':
    for f in files:
        print(f"Processing {f}...")
        process_file(f)
    print("All files enhanced.")