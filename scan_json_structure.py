
import json

# Path to your TN election JSON file
json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()))

if "results" in data:
    years = list(data["results"].keys())
    print("Years:", years)
    for year in years:
        counties = list(data["results"][year].keys())
        print(f"\nYear: {year} | Counties: {len(counties)}")
        if not counties:
            print("  No counties found for this year.")
            continue
        first_county = counties[0]
        contests = list(data["results"][year][first_county].keys())
        print(f"Sample county: {first_county} | Contests: {contests}")
        if contests:
            first_contest = contests[0]
            print("Sample contest result:", json.dumps(data["results"][year][first_county][first_contest], indent=2))
else:
    print("Sample data:", json.dumps(data, indent=2)[:1000])