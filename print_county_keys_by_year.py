import json

json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

def print_county_keys(year):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    counties = results.get(year, {})
    print(f"County keys for {year}:")
    for county in sorted(counties.keys()):
        print(county)
    print(f"Total counties: {len(counties)}")

if __name__ == "__main__":
    for year in ["2008", "2010", "2012"]:
        print_county_keys(year)
