import json

# Path to the filtered TN election JSON
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

def scan_missing(year):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    missing_counties = []
    all_counties = set()
    # Get all counties present in any year for reference
    for y, counties in results.items():
        all_counties.update(counties.keys())
    missing_in_year = sorted(all_counties - set(results.get(year, {}).keys()))
    print(f"Counties missing contest data in {year}:")
    for county in missing_in_year:
        print(county)
    if not missing_in_year:
        print(f"All counties have contest data for {year}.")

if __name__ == "__main__":
    for year in ["2008", "2010", "2012"]:
        scan_missing(year)
