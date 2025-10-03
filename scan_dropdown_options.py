import json

# Path to your existing dropdown JSON
json_path = "Election_Data/standardized/tn_contest_year_dropdown.json"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        dropdown = json.load(f)
    print("Dropdown options:")
    for label in dropdown:
        print("  ", label)
    print(f"Total options: {len(dropdown)}")

if __name__ == "__main__":
    main()
