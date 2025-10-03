import json

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_contests = set()
    for year, counties in data.get("results", {}).items():
        for county, contests in counties.items():
            for contest in contests.keys():
                all_contests.add(contest)
    print("All contest names found in merged JSON:")
    for contest in sorted(all_contests):
        print("  ", contest)
    print(f"Total unique contests: {len(all_contests)}")

if __name__ == "__main__":
    main()
