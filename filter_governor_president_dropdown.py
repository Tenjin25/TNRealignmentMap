import json

# Path to the filtered JSON file (governor and president only)
data_path = "Election_Data/standardized/tn_governor_president_only.json"
# Path to the contest-year dropdown json
dropdown_path = "Election_Data/standardized/tn_contest_year_dropdown.json"
# Output path for filtered dropdown
output_path = "Election_Data/standardized/tn_governor_president_dropdown.json"

# Contests to keep (case-insensitive, substring match)
KEEP_CONTESTS = ["governor", "president"]

def normalize_contest(name):
    return name.lower().replace("_", " ").replace(".", "").strip()

def is_keep_contest(name):
    norm = normalize_contest(name)
    for key in KEEP_CONTESTS:
        if key in norm:
            return True
    return False

def main():
    with open(dropdown_path, "r", encoding="utf-8") as f:
        dropdown = json.load(f)
    # Only keep dropdown options that match governor or president
    filtered_dropdown = []
    for label in dropdown:
        contest = label.split(" (")[0]
        if is_keep_contest(contest):
            filtered_dropdown.append(label)
    # Save filtered dropdown
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_dropdown, f, indent=2, ensure_ascii=False)
    print(f"Filtered dropdown saved to {output_path}")

if __name__ == "__main__":
    main()
