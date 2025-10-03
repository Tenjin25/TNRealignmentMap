import json
import csv
import os
import re
import glob
import argparse
from collections import Counter

# Set a high limit for CSV field sizes to handle large data cells
csv.field_size_limit(10**7)

# --- Utility Functions ---

def load_json(path):
    """Loads a JSON file from the given path."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    """Saves data to a JSON file with indentation."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def margin_label(dem_votes, rep_votes, margin_pct):
    """Creates a human-readable margin label like 'D+5.20' or 'R+10.00'."""
    if dem_votes > rep_votes:
        return f"D+{abs(margin_pct):.2f}"
    elif rep_votes > dem_votes:
        return f"R+{abs(margin_pct):.2f}"
    else:
        return "Tied"

def get_competitiveness(margin_pct):
    """
    Determines the competitiveness category, party, color, and code based on the margin percentage.
    This is the single source of truth for competitiveness logic.
    """
    abs_margin = abs(margin_pct)
    
    # Tossup is a special case
    if -0.5 <= margin_pct <= 0.5:
        return {"category": "Tossup", "party": "Tossup", "code": "TOSSUP", "color": "#f7f7f7"}

    # Republican scale
    if margin_pct < -0.5: # Negative margin means Republican win
        party = "Republican"
        if abs_margin >= 40.0: cat, color, code = "Annihilation", "#67000d", "R_ANNIHILATION"
        elif abs_margin >= 30.0: cat, color, code = "Dominant", "#a50f15", "R_DOMINANT"
        elif abs_margin >= 20.0: cat, color, code = "Stronghold", "#cb181d", "R_STRONGHOLD"
        elif abs_margin >= 10.0: cat, color, code = "Safe", "#ef3b2c", "R_SAFE"
        elif abs_margin >= 5.5:  cat, color, code = "Likely", "#fb6a4a", "R_LIKELY"
        elif abs_margin >= 1.0:  cat, color, code = "Lean", "#fcae91", "R_LEAN"
        else:                    cat, color, code = "Tilt", "#fee8c8", "R_TILT" # 0.5 to 1.0
        return {"category": cat, "party": party, "code": code, "color": color}

    # Democratic scale
    if margin_pct > 0.5: # Positive margin means Democratic win
        party = "Democratic"
        if abs_margin >= 40.0: cat, color, code = "Annihilation", "#08306b", "D_ANNIHILATION"
        elif abs_margin >= 30.0: cat, color, code = "Dominant", "#08519c", "D_DOMINANT"
        elif abs_margin >= 20.0: cat, color, code = "Stronghold", "#3182bd", "D_STRONGHOLD"
        elif abs_margin >= 10.0: cat, color, code = "Safe", "#6baed6", "D_SAFE"
        elif abs_margin >= 5.5:  cat, color, code = "Likely", "#9ecae1", "D_LIKELY"
        elif abs_margin >= 1.0:  cat, color, code = "Lean", "#c6dbef", "D_LEAN"
        else:                    cat, color, code = "Tilt", "#e1f5fe", "D_TILT" # 0.5 to 1.0
        return {"category": cat, "party": party, "code": code, "color": color}
    
    return {"category": "", "party": "", "code": "", "color": ""}


# --- Core Parsing and Aggregation Logic ---

def parse_csv(path, contests_of_interest=None):
    """
    Parses a standardized election CSV, aggregates results by (county, contest),
    and calculates margins and competitiveness.
    """
    if contests_of_interest is None:
        contests_of_interest = ["GOVERNOR", "PRESIDENT", "SENATE", "HOUSE"]

    agg = {} # Aggregate by (county, contest)
    PARTY_MAP = {
        'D': 'DEM', 'DEM': 'DEM', 'DEMOCRAT': 'DEM', 'DEMOCRATIC': 'DEM',
        'R': 'REP', 'REP': 'REP', 'REPUBLICAN': 'REP',
        'L': 'LIB', 'LIB': 'LIB', 'LIBERTARIAN': 'LIB',
        'G': 'GRN', 'GRN': 'GRN', 'GREEN': 'GRN',
        'I': 'IND', 'IND': 'IND', 'INDEPENDENT': 'IND',
    }
    
    def normalize_name(name):
        return re.sub(r"\s+", " ", name.strip().upper())
        
    def contest_matches(contest, interested):
        """
        Flexible matching for contests of interest.
        Note: Substring matching can have false positives (e.g., 'HOUSE' in 'WHITE HOUSE').
        """
        c = normalize_name(contest)
        for i in interested:
            i_norm = normalize_name(i)
            if i_norm in c or c in i_norm: return True
            if i_norm.startswith('PRESIDENT') and 'PRESIDENT' in c: return True
        return False
        
    def shorten_pres_candidate(name):
        """Helper to shorten longform presidential candidate names."""
        if 'ELECTORS FOR' in name.upper() and 'PRESIDENT' in name.upper():
            m = re.search(r'for ([A-Za-z .\'-]+) for President', name, re.IGNORECASE)
            if m: return m.group(1).strip()
        return name

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
        field_map = {k.lower(): k for k in reader.fieldnames}

        def find_field(*candidates):
            for c in candidates:
                if c.lower() in field_map: return field_map[c.lower()]
            return None

        # Dynamically find column names
        county_field = find_field("county")
        contest_field = find_field("candidate_group", "contest", "office", "officename")
        party_field = find_field("party")
        votes_field = find_field("votes")
        candidate_field = find_field("candidate")

        if not all([county_field, contest_field, votes_field]):
            raise ValueError(f"Required columns (county, contest, votes) not found in {path}. Found: {reader.fieldnames}")

        for row in reader:
            county = normalize_name(row[county_field])
            contest = normalize_name(row[contest_field])

            if not contest_matches(contest, contests_of_interest):
                continue
            
            party_val = normalize_name(row.get(party_field, "")) if party_field else ""
            party_val = PARTY_MAP.get(party_val, party_val)

            candidate_val = row.get(candidate_field, "").strip() if candidate_field else ""
            if '2024' in path and 'PRESIDENT' in contest:
                candidate_val = shorten_pres_candidate(candidate_val)

            try:
                votes_val = int(float(row.get(votes_field, 0)))
            except (ValueError, TypeError):
                votes_val = 0

            key = (county, contest)
            if key not in agg:
                agg[key] = {
                    "dem_votes": 0, "rep_votes": 0, "other_votes": 0, "total_votes": 0,
                    "all_parties": {}, "candidates": {}, "dem_candidate": None, "rep_candidate": None,
                }
            
            # Aggregate votes
            agg[key]["total_votes"] += votes_val
            if candidate_val:
                agg[key]["candidates"].setdefault(candidate_val, 0)
                agg[key]["candidates"][candidate_val] += votes_val
            if party_val:
                agg[key]["all_parties"].setdefault(party_val, 0)
                agg[key]["all_parties"][party_val] += votes_val

            if party_val.startswith("DEM"):
                agg[key]["dem_votes"] += votes_val
                # Note: This assigns the first Dem candidate found. May not be the top vote-getter.
                if agg[key]["dem_candidate"] is None:
                    agg[key]["dem_candidate"] = candidate_val
            elif party_val.startswith("REP"):
                agg[key]["rep_votes"] += votes_val
                if agg[key]["rep_candidate"] is None:
                    agg[key]["rep_candidate"] = candidate_val
            else:
                agg[key]["other_votes"] += votes_val

    # --- Process aggregated data into final county dictionary ---
    counties = {}
    print(f"\n--- Processing results from: {os.path.basename(path)} ---")
    contest_counter = Counter(contest for _, contest in agg.keys())
    print(f"Found {len(contest_counter)} unique contests of interest.")

    for (county, contest), vals in agg.items():
        dem_votes = vals["dem_votes"]
        rep_votes = vals["rep_votes"]
        two_party_total = dem_votes + rep_votes
        margin = dem_votes - rep_votes
        margin_pct = (margin * 100 / two_party_total) if two_party_total > 0 else 0.0

        result = {
            "dem_votes": dem_votes,
            "rep_votes": rep_votes,
            "other_votes": vals["other_votes"],
            "total_votes": vals["total_votes"],
            "margin": margin,
            "margin_pct": margin_pct,
            "margin_label": margin_label(dem_votes, rep_votes, margin_pct),
            "winner": "DEM" if dem_votes > rep_votes else ("REP" if rep_votes > dem_votes else "TOSSUP"),
            "all_parties": vals["all_parties"],
            "candidates": vals["candidates"],
            "dem_candidate": vals.get("dem_candidate"),
            "rep_candidate": vals.get("rep_candidate"),
            "competitiveness": get_competitiveness(margin_pct)
        }
        
        if county not in counties:
            counties[county] = {}
        counties[county][contest] = result
        
    return counties


# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Merge standardized CSV election data into a structured JSON format.")
    parser.add_argument("--csv", help="Path to a single standardized CSV file.")
    parser.add_argument("--csv-dir", help="Directory containing standardized CSVs for one or more years.")
    parser.add_argument("--stable-output", required=True, help="Path to output a stable-keyed JSON file for all years.")
    parser.add_argument("--contests", help="Comma-separated list of contests to process (e.g., 'PRESIDENT,SENATE').")
    args = parser.parse_args()

    if not args.csv and not args.csv_dir:
        raise ValueError("You must provide either --csv or --csv-dir.")

    if args.csv_dir:
        all_csvs = sorted(glob.glob(os.path.join(args.csv_dir, '*.csv')))
    else:
        all_csvs = [args.csv]

    print(f"Found {len(all_csvs)} CSV files to process.")
    
    # Optional override for contests of interest
    contests_of_interest = args.contests.split(',') if args.contests else None

    # --- Single Processing Loop ---
    # This loop processes each CSV file ONCE and builds the final data structure.
    stable_results_by_year = {}

    def extract_year_from_filename(filename):
        m = re.search(r'(20\d{2})', os.path.basename(filename))
        return m.group(1) if m else None

    def contest_type_from_name(contest):
        c = contest.strip().upper()
        if "PRESIDENT" in c: return "presidential"
        if "SENATE" in c: return "senate"
        if "HOUSE" in c: return "house"
        if "GOVERNOR" in c: return "governor"
        return "other"

    for csvfile in all_csvs:
        year = extract_year_from_filename(csvfile)
        if not year:
            print(f"Warning: Could not determine year from filename, skipping: {csvfile}")
            continue

        # Parse the entire CSV for county-level results
        # The parse_csv function handles aggregation and all calculations.
        counties_data = parse_csv(csvfile, contests_of_interest)
        
        # Structure the parsed data into the stable format
        for county, contests in counties_data.items():
            for contest, result in contests.items():
                ctype = contest_type_from_name(contest)
                key = f"{ctype}_{year}_{contest.replace(' ', '_')}" # Create a stable key
                
                # Initialize nested dictionaries if they don't exist
                stable_results_by_year.setdefault(year, {}).setdefault(ctype, {}).setdefault(key, {
                    "contest_name": contest,
                    "results": {}
                })
                
                # Add extra metadata and store the result
                output_result = dict(result)
                output_result["county"] = county
                output_result["contest"] = contest
                output_result["year"] = year
                stable_results_by_year[year][ctype][key]["results"][county] = output_result
    
    # Save the final aggregated data
    if args.stable_output:
        final_data = {"results_by_year": stable_results_by_year}
        save_json(final_data, args.stable_output)
        print(f"\n✅ Success! Wrote stable-keyed county results for all years to {args.stable_output}")


if __name__ == "__main__":
    main()