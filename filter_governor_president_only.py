import json

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"
output_path = "Election_Data/standardized/tn_governor_president_only.json"

# Contests to keep (case-insensitive, substring match)
KEEP_CONTESTS = ["governor", "president"]

def normalize_contest(name):
    return name.lower().replace("_", " ").replace(".", "").strip()

def is_keep_contest(name):
    norm = normalize_contest(name)
    for key in KEEP_CONTESTS:
        if key in norm:
            return True
    return False

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    filtered_data = json.loads(json.dumps(data))  # Deep copy
    # Filter for governor and president only
    for year, counties in filtered_data.get("results", {}).items():
        for county, contests in counties.items():
            keys_to_remove = [c for c in contests if not is_keep_contest(c)]
            for k in keys_to_remove:
                contests.pop(k)
    # Save filtered JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    print(f"Filtered JSON with only governor and president contests saved to {output_path}")

if __name__ == "__main__":
    main()
