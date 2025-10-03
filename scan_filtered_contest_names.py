import json

# Path to the filtered JSON file
json_path = "Election_Data/standardized/tn_governor_president_senate_only.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_contests = set()
    for year, counties in data.get("results", {}).items():
        for county, contests in counties.items():
            for contest in contests.keys():
                all_contests.add(contest)
    print("All contest names found in filtered JSON:")
    for contest in sorted(all_contests):
        print("  ", contest)
    print(f"Total unique contests: {len(all_contests)}")

if __name__ == "__main__":
    main()
