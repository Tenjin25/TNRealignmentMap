import json

# Path to the filtered JSON file
json_path = "Election_Data/standardized/tn_display_contests_only.json"
# Output path for contest-year pairs
output_path = "Election_Data/standardized/tn_contest_year_dropdown.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    contest_year_set = set()
    # Scan all years and contests
    for year, counties in data.get("results", {}).items():
        for county, contests in counties.items():
            for contest in contests.keys():
                # Format: "Contest Name (Year)" with title case
                label = f"{contest.replace('_', ' ').title()} ({year})"
                contest_year_set.add(label)
    # Sort for dropdown
    contest_year_list = sorted(contest_year_set)
    # Print for review
    print("Contest-Year Dropdown Options:")
    for label in contest_year_list:
        print("  ", label)
    # Save as JSON array
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(contest_year_list, f, indent=2, ensure_ascii=False)
    print(f"Dropdown options saved to {output_path}")

if __name__ == "__main__":
    main()
