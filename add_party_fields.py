# Script to add 'party' and 'competitiveness_winner' fields to TN election results JSON
import json

INPUT_PATH = 'Election_Data/standardized/tn_legacy_comprehensive_by_county.json'
OUTPUT_PATH = 'Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json'

def assign_party_fields(result):
    # Assign winning party
    dem = result.get('dem_votes', 0)
    rep = result.get('rep_votes', 0)
    if dem > rep:
        result['party'] = 'DEM'
    elif rep > dem:
        result['party'] = 'REP'
    else:
        result['party'] = 'TIE'
    # Assign competitiveness_winner based on margin
    margin = result.get('margin_pct', 0)
    if margin > 0.5:
        result['competitiveness_winner'] = 'Republican'
    elif margin < -0.5:
        result['competitiveness_winner'] = 'Democratic'
    else:
        result['competitiveness_winner'] = 'Tossup'
    return result

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for year, counties in data.get('results', {}).items():
        for county, contests in counties.items():
            for contest, result in contests.items():
                assign_party_fields(result)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Updated file written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
