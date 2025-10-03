import json

# Path to the merged JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for year in ["2008", "2010", "2012"]:
        print(f"\nContests found in {year}:")
        contests_set = set()
        counties = data.get("results", {}).get(year, {})
        for county, contests in counties.items():
            for contest in contests.keys():
                contests_set.add(contest)
        for contest in sorted(contests_set):
            print("  ", contest)
        if not contests_set:
            print("  (No contests found)")

if __name__ == "__main__":
    main()
