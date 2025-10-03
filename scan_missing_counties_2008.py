import json

# Path to the filtered TN election JSON
json_path = "Election_Data/standardized/tn_governor_president_senate_only.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    year = "2008"
    missing_counties = []
    for county in sorted(results.get(year, {})):
        contests = results[year][county]
        if not contests:
            missing_counties.append(county)
    all_counties = set()
    # Get all counties present in any year for reference
    for y, counties in results.items():
        all_counties.update(counties.keys())
    missing_in_2008 = sorted(all_counties - set(results.get(year, {}).keys()))
    print(f"Counties missing contest data in 2008:")
    for county in missing_in_2008:
        print(county)
    if not missing_in_2008:
        print("All counties have contest data for 2008.")

if __name__ == "__main__":
    main()
