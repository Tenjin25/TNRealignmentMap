import json

# Path to the filtered JSON file
json_path = "Election_Data/standardized/tn_governor_president_senate_only.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Filtered contest names by year:")
    for year, counties in data.get("results", {}).items():
        contests_set = set()
        for county, contests in counties.items():
            for contest in contests.keys():
                contests_set.add(contest)
        print(f"{year}:")
        for contest in sorted(contests_set):
            print(f"  {contest}")
        if not contests_set:
            print("  (No contests found)")

if __name__ == "__main__":
    main()
