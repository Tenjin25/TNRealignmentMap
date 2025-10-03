import json
from collections import defaultdict

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

# Contests to display in frontend (case-insensitive, substring match)
DISPLAY_CONTESTS = [
    "governor",
    "president",
    "united_states_president",
    "president_and_vice_president_of_the_united_states",
    "us senate",
    "united_states_senate",
    "senate"
]

# Output filtered JSON for frontend
output_path = "Election_Data/standardized/tn_display_contests_only.json"

# Helper: normalize contest name for matching

def normalize_contest(name):
    return name.lower().replace("_", " ").replace("-", " ").strip()

def is_display_contest(name):
    norm = normalize_contest(name)
    for key in DISPLAY_CONTESTS:
        if key in norm:
            return True
    return False

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_contests = set()
    filtered_data = json.loads(json.dumps(data))  # Deep copy
    # Scan all contests
    for year, counties in data.get("results", {}).items():
        for county, contests in counties.items():
            for contest in contests.keys():
                all_contests.add(contest)
    print("All contest names found:")
    for contest in sorted(all_contests):
        print("  ", contest)
    # Filter for display contests only and remove date labels
    date_labels = {"november 2", "november 4", "november 6"}
    for year, counties in filtered_data.get("results", {}).items():
        for county, contests in counties.items():
            keys_to_remove = [c for c in contests if not is_display_contest(c) or normalize_contest(c) in date_labels]
            for k in keys_to_remove:
                contests.pop(k)
    # Save filtered JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    print(f"Filtered JSON with only display contests saved to {output_path}")

if __name__ == "__main__":
    main()
