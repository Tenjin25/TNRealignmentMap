import json

json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

def print_contest_data(year, counties):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    for county in counties:
        print(f"County: {county}")
        contests = results.get(year, {}).get(county, {})
        if contests:
            for contest, contest_data in contests.items():
                print(f"  Contest: {contest}")
                print(f"    Data: {contest_data}")
        else:
            print("  No contest data found.")
        print()

if __name__ == "__main__":
    # Check a few counties for 2008, 2010, 2012
    sample_counties = ["Anderson", "Shelby", "Knox", "Hamilton", "Davidson"]
    for year in ["2008", "2010", "2012"]:
        print(f"--- {year} ---")
        print_contest_data(year, sample_counties)
