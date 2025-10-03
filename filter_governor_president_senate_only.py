import json

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"
output_path = "Election_Data/standardized/tn_governor_president_senate_only.json"

KEEP_CONTESTS = [
    "Governor",
    "governor",
    "President",
    "president",
    "president_and_vice_president_of_the_united_states",
    "United States President",
    "united_states_president",
    "United States Senate",
    "united_states_senate",
    "senate"
]

def normalize_contest(name):
    return name.lower().replace("_", " ").replace(".", "").strip()

def is_keep_contest(name):
    # Match exact or normalized contest names
    norm = normalize_contest(name)
    for key in KEEP_CONTESTS:
        if name == key or norm == key.lower().replace("_", " ").replace(".", "").strip():
            return True
    return False

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    filtered_data = json.loads(json.dumps(data))  # Deep copy
    # Filter for governor, president, and senate only
    for year, counties in filtered_data.get("results", {}).items():
        for county, contests in counties.items():
            keys_to_remove = [c for c in contests if not is_keep_contest(c)]
            for k in keys_to_remove:
                contests.pop(k)
    # Save filtered JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    print(f"Filtered JSON with only governor, president, and senate contests saved to {output_path}")

if __name__ == "__main__":
    main()
