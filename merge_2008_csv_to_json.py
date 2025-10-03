import json
import csv
import os

# Paths
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json"
csv_path = "Election_Data/standardized/2008_standardized_long.csv"
output_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"
missing_year = "2008"

# Load existing JSON
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Parse CSV and build county results
# Assumes columns: year,county,contest,dem_votes,rep_votes,other_votes,total_votes,two_party_total,margin,margin_pct,winner,all_parties,candidates,competitiveness_category,competitiveness_color,party,competitiveness_winner

def parse_csv(path):
    counties = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = row["county"].strip()
            contest = row["contest"].strip()
            # Parse numeric fields
            def to_int(val):
                try:
                    return int(val)
                except:
                    return 0
            def to_float(val):
                try:
                    return float(val)
                except:
                    return 0.0
            # Parse JSON fields
            def to_json(val):
                try:
                    return json.loads(val.replace("'", '"'))
                except:
                    return {}
            result = {
                "dem_votes": to_int(row.get("dem_votes", 0)),
                "rep_votes": to_int(row.get("rep_votes", 0)),
                "other_votes": to_int(row.get("other_votes", 0)),
                "total_votes": to_int(row.get("total_votes", 0)),
                "two_party_total": to_int(row.get("two_party_total", 0)),
                "margin": to_int(row.get("margin", 0)),
                "margin_pct": to_float(row.get("margin_pct", 0)),
                "winner": row.get("winner", "").strip(),
                "all_parties": to_json(row.get("all_parties", "{}")),
                "candidates": to_json(row.get("candidates", "{}")),
                "competitiveness_category": row.get("competitiveness_category", "").strip(),
                "competitiveness_color": row.get("competitiveness_color", "").strip(),
                "party": row.get("party", "").strip(),
                "competitiveness_winner": row.get("competitiveness_winner", "").strip()
            }
            if county not in counties:
                counties[county] = {}
            counties[county][contest] = result
    return counties

def main():
    data = load_json(json_path)
    counties = parse_csv(csv_path)
    # Insert into JSON structure
    if "results" not in data:
        print("Error: 'results' key not found in JSON.")
        return
    data["results"][missing_year] = counties
    save_json(data, output_path)
    print(f"Merged {len(counties)} counties for {missing_year} into {output_path}")

if __name__ == "__main__":
    main()
