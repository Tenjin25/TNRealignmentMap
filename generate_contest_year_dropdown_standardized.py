import json

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"
# Output path for contest-year pairs
output_path = "Election_Data/standardized/tn_contest_year_dropdown.json"

# Standardize contest names mapping
CONTEST_NAME_MAP = {
    "united states president": "President",
    "president and vice president of the united states": "President",
    "united states senate": "US Senate",
    "governor": "Governor"
}

def standardize_contest_name(name):
    norm = name.lower().replace("_", " ").strip()
    return CONTEST_NAME_MAP.get(norm, name.title())

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    contest_year_set = set()
    # Scan all years and contests
    for year, counties in data.get("results", {}).items():
        for county, contests in counties.items():
            for contest in contests.keys():
                label = f"{standardize_contest_name(contest)} ({year})"
                contest_year_set.add(label)
    # Sort for dropdown
    contest_year_list = sorted(contest_year_set)
    # Print for review
    print("Contest-Year Dropdown Options:")
    for label in contest_year_list:
        print("  ", label)
    # Save as JSON array
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(contest_year_list, f, indent=2, ensure_ascii=False)
    print(f"Dropdown options saved to {output_path}")

if __name__ == "__main__":
    main()
