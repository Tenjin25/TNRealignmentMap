
import pandas as pd
import os
import glob
import json
import re

STANDARDIZED_DIR = os.path.join('Election_Data', 'standardized')


# Include all *_enhanced.csv and *_long.csv files

pattern1 = os.path.join(STANDARDIZED_DIR, '*_enhanced.csv')
pattern2 = os.path.join(STANDARDIZED_DIR, '*_long.csv')
files = glob.glob(pattern1) + glob.glob(pattern2)
# Sort files by year (2004-2024)
def extract_year(f):
    try:
        y = int(os.path.basename(f)[:4])
        if 2004 <= y <= 2024:
            return y
    except Exception:
        pass
    return 9999  # push non-matching files to end
files = sorted(files, key=extract_year)



combined = {}
all_office_names = set()

for f in files:
    year = os.path.basename(f)[:4]
    df = pd.read_csv(f, dtype=str)
    # Normalize column names
    df.columns = [c.strip().upper() for c in df.columns]
    # Ensure numeric fields are correct
    if 'VOTES' in df.columns:
        df['VOTES'] = pd.to_numeric(df['VOTES'], errors='coerce').fillna(0).astype(int)
    # Helper to sanitize contest names
    def sanitize(name):
        name = str(name).strip()
        name = re.sub(r'[\\/\?]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name
    # Print all unique contest names for diagnostics
    contest_col = None
    for col in ['OFFICENAME', 'OFFICE']:
        if col in df.columns:
            sample_vals = df[col].dropna().astype(str).head(10).tolist()
            if not all(re.match(r'\s*"?November \d+', v) for v in sample_vals):
                contest_col = col
                break
    if contest_col:
        all_office_names.update(df[contest_col].dropna().unique())
        sanitized_names = set(sanitize(n) for n in df[contest_col].dropna().unique())
        print(f"Year {year}: unique sanitized {contest_col} values:")
        for n in sorted(sanitized_names):
            print(f"  - {n}")
    if year not in combined:
        combined[year] = {}
    if 'COUNTY' in df.columns and contest_col and 'PARTY' in df.columns:
        # Use sanitized contest name matches for President, US Senate, and Governor
        target_offices = set([
            sanitize('United States President'),
            sanitize('President and Vice President of the United States'),
            sanitize('United States Senate'),
            sanitize('Governor'),
            sanitize('President')
        ])
        for (county, contest), group in df.groupby(['COUNTY', contest_col]):
            contest_clean = sanitize(contest)
            if contest_clean not in target_offices:
                continue
            county_key = str(county).strip().replace(' ', '_').upper()
            contest_key = re.sub(r'[\\/\?]', '', contest_clean.replace(' ', '_')).lower()
            if county_key not in combined[year]:
                combined[year][county_key] = {}
            if contest_key not in combined[year][county_key]:
                combined[year][county_key][contest_key] = {}
            # Normalize party codes
            def normalize_party(p):
                p = str(p).strip().upper()
                if p in ['D', 'DEM', 'DEMOCRAT', 'DEMOCRATIC']:
                    return 'DEM'
                if p in ['R', 'REP', 'REPUBLICAN']:
                    return 'REP'
                return p.title() if p else p

            # Aggregate votes by normalized party
            group['PARTY_NORM'] = group['PARTY'].map(normalize_party)
            party_votes = group.groupby('PARTY_NORM')['VOTES'].sum().to_dict()

            # Collect candidate names for each normalized party
            candidates = {}
            if 'CANDIDATE' in group.columns:
                for party, subdf in group.groupby('PARTY_NORM'):
                    # Get unique candidate names, dropna, strip whitespace
                    names = sorted(set(str(n).strip() for n in subdf['CANDIDATE'].dropna() if str(n).strip()))
                    candidates[party] = names
            else:
                # If no candidate column, leave empty dict
                candidates = {}

            # Calculate dem_votes, rep_votes, other_votes, total_votes, two_party_total, margin, margin_pct, winner
            dem_votes = party_votes.get('DEM', 0)
            rep_votes = party_votes.get('REP', 0)
            other_votes = sum(v for p, v in party_votes.items() if p not in ['DEM', 'REP'])
            total_votes = sum(party_votes.values())
            two_party_total = dem_votes + rep_votes
            margin = rep_votes - dem_votes
            margin_pct = ((margin / two_party_total) * 100) if two_party_total else 0
            winner = 'REP' if rep_votes > dem_votes else ('DEM' if dem_votes > rep_votes else 'TIE')
            combined[year][county_key][contest_key] = {
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': round(margin_pct, 2),
                'winner': winner,
                'all_parties': party_votes,
                'candidates': candidates
            }

print("Unique OFFICENAME values found across all files:")
for name in sorted(all_office_names):
    print(f"- {name}")


# Define competitiveness scale
competitiveness_scale = {
    "Republican": [
        {"category": "Annihilation", "range": "R+40%+", "color": "#67000d", "min": 40.0, "max": 100.0},
        {"category": "Dominant", "range": "R+30-40%", "color": "#a50f15", "min": 30.0, "max": 40.0},
        {"category": "Stronghold", "range": "R+20-30%", "color": "#cb181d", "min": 20.0, "max": 30.0},
        {"category": "Safe", "range": "R+10-20%", "color": "#ef3b2c", "min": 10.0, "max": 20.0},
        {"category": "Likely", "range": "R+5.5-10%", "color": "#fb6a4a", "min": 5.5, "max": 10.0},
        {"category": "Lean", "range": "R+1-5.5%", "color": "#fcae91", "min": 1.0, "max": 5.5},
        {"category": "Tilt", "range": "R+0.5-1%", "color": "#fee8c8", "min": 0.5, "max": 1.0}
    ],
    "Tossup": [
        {"category": "Tossup", "range": "±0.5%", "color": "#f7f7f7", "min": -0.5, "max": 0.5}
    ],
    "Democratic": [
        {"category": "Tilt", "range": "D+0.5-1%", "color": "#e1f5fe", "min": -1.0, "max": -0.5},
        {"category": "Lean", "range": "D+1-5.5%", "color": "#c6dbef", "min": -5.5, "max": -1.0},
        {"category": "Likely", "range": "D+5.5-10%", "color": "#9ecae1", "min": -10.0, "max": -5.5},
        {"category": "Safe", "range": "D+10-20%", "color": "#6baed6", "min": -20.0, "max": -10.0},
        {"category": "Stronghold", "range": "D+20-30%", "color": "#3182bd", "min": -30.0, "max": -20.0},
        {"category": "Dominant", "range": "D+30-40%", "color": "#08519c", "min": -40.0, "max": -30.0},
        {"category": "Annihilation", "range": "D+40%+", "color": "#08306b", "min": -100.0, "max": -40.0}
    ]
}

# Helper to assign competitiveness category and color
def get_competitiveness(margin_pct, winner):
    if winner == 'TIE' or abs(margin_pct) <= 0.5:
        return ('Tossup', '#f7f7f7')
    if winner == 'REP':
        for entry in competitiveness_scale['Republican']:
            if margin_pct >= entry['min'] and margin_pct < entry['max']:
                return (entry['category'], entry['color'])
    if winner == 'DEM':
        for entry in competitiveness_scale['Democratic']:
            if margin_pct <= entry['max'] and margin_pct > entry['min']:
                return (entry['category'], entry['color'])
    return ('Unknown', '#cccccc')

# Add competitiveness info to each contest result
for year in combined:
    for county in combined[year]:
        for contest in combined[year][county]:
            result = combined[year][county][contest]
            cat, color = get_competitiveness(result['margin_pct'], result['winner'])
            result['competitiveness_category'] = cat
            result['competitiveness_color'] = color

# Write output with competitiveness_scale as top-level key
output_path = os.path.join(STANDARDIZED_DIR, 'tn_legacy_comprehensive_by_county.json')
output_obj = {
    'competitiveness_scale': competitiveness_scale,
    'results': combined
}
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_obj, f, indent=2, ensure_ascii=False)

print(f"Combined JSON written to {output_path}")
