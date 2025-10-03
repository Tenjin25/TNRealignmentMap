import csv
csv.field_size_limit(10**7)
import json
import os
import re
from collections import defaultdict

# List of CSVs to process (update as needed)
CSV_FILES = [
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2006_standardized_governor_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2006_standardized_senate_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\CSVs\20041102__tn__general__precinct.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\20121106__tn__general__precinct.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\20081104__tn__general__precinct.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\20101102__tn__general__precinct.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2024_standardized_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2022_standardized_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2020_standardized_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2018_standardized_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2016_standardized_long.csv",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\standardized\2014_standardized_long.csv"
]

CATEGORIZATION_SYSTEM = {
    "competitiveness_scale": {
        "Republican": [
            {"category": "Annihilation", "range": "R+40%+", "color": "#67000d"},
            {"category": "Dominant", "range": "R+30-40%", "color": "#a50f15"},
            {"category": "Stronghold", "range": "R+20-30%", "color": "#cb181d"},
            {"category": "Safe", "range": "R+10-20%", "color": "#ef3b2c"},
            {"category": "Likely", "range": "R+5.5-10%", "color": "#fb6a4a"},
            {"category": "Lean", "range": "R+1-5.5%", "color": "#fcae91"},
            {"category": "Tilt", "range": "R+0.5-1%", "color": "#fee8c8"}
        ],
        "Tossup": [
            {"category": "Tossup", "range": "±0.5%", "color": "#f7f7f7"}
        ],
        "Democratic": [
            {"category": "Tilt", "range": "D+0.5-1%", "color": "#e1f5fe"},
            {"category": "Lean", "range": "D+1-5.5%", "color": "#c6dbef"},
            {"category": "Likely", "range": "D+5.5-10%", "color": "#9ecae1"},
            {"category": "Safe", "range": "D+10-20%", "color": "#6baed6"},
            {"category": "Stronghold", "range": "D+20-30%", "color": "#3182bd"},
            {"category": "Dominant", "range": "D+30-40%", "color": "#08519c"},
            {"category": "Annihilation", "range": "D+40%+", "color": "#08306b"}
        ]
    },
    "office_types": ["Federal", "State", "Judicial", "Other"],
    "enhanced_features": [
        "Competitiveness categorization for each precinct",
        "Contest type classification (Federal/State/Judicial)",
        "Office ranking system for analysis prioritization",
        "Color coding compatible with political geography visualization"
    ]
}

# Utility functions
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

def margin_label(dem_votes, rep_votes, margin_pct):
    if dem_votes > rep_votes:
        return f"D+{abs(margin_pct):.2f}"
    elif rep_votes > dem_votes:
        return f"R+{abs(margin_pct):.2f}"
    else:
        return "Tied"

def get_display_contest_name(normalized_contest):
    """Get clean display name for normalized contest"""
    display_names = {
        "PRESIDENT": "President",
        "US_SENATE": "U.S. Senate", 
        "GOVERNOR": "Governor",
        "US_HOUSE": "U.S. House",
        "STATE_HOUSE": "State House",
        "STATE_SENATE": "State Senate"
    }
    return display_names.get(normalized_contest, normalized_contest.title())

def normalize_contest_name(contest_name):
    """Normalize contest names to group similar contests together"""
    contest = contest_name.upper().strip()
    
    # Normalize Presidential contests
    if any(word in contest for word in ["PRESIDENT", "VICE PRESIDENT"]):
        return "PRESIDENT"
    
    # Normalize US Senate contests  
    if any(phrase in contest for phrase in ["U.S. SENATE", "US SENATE", "UNITED STATES SENATE"]):
        return "US_SENATE"
    
    # Normalize Governor contests
    if "GOVERNOR" in contest:
        return "GOVERNOR"
    
    # Normalize US House contests
    if any(phrase in contest for phrase in ["U.S. HOUSE", "US HOUSE", "UNITED STATES HOUSE"]):
        return "US_HOUSE"
        
    # Normalize State House contests
    if any(phrase in contest for phrase in ["STATE HOUSE", "TENNESSEE HOUSE"]):
        return "STATE_HOUSE"
        
    # Normalize State Senate contests
    if any(phrase in contest for phrase in ["STATE SENATE", "TENNESSEE SENATE"]):
        return "STATE_SENATE"
    
    # Return original if no normalization rule matches
    return contest

def contest_type_from_name(contest_name):
    """Determine contest type based on normalized contest name"""
    if contest_name in ["PRESIDENT", "US_SENATE", "US_HOUSE"]:
        return "federal"
    elif contest_name == "GOVERNOR":
        return "governor"
    elif contest_name in ["STATE_HOUSE", "STATE_SENATE"]:
        return "state"
    else:
        return "other"

def get_competitiveness_category(margin_pct):
    """Get full competitiveness category information"""
    abs_margin = abs(margin_pct)
    
    if abs_margin < 0.5:
        return {
            "category": "Tossup", 
            "party": "Tossup",
            "code": "TOSSUP",
            "color": "#f7f7f7"
        }
    
    # Determine party
    party = "Republican" if margin_pct < 0 else "Democratic"
    party_code = "REP" if margin_pct < 0 else "DEM"
    
    if abs_margin < 1:
        category = "Tilt"
        color = "#fee8c8" if party == "Republican" else "#e1f5fe"
    elif abs_margin < 5.5:
        category = "Lean"
        color = "#fcae91" if party == "Republican" else "#c6dbef"
    elif abs_margin < 10:
        category = "Likely"
        color = "#fb6a4a" if party == "Republican" else "#9ecae1"
    elif abs_margin < 20:
        category = "Safe"
        color = "#ef3b2c" if party == "Republican" else "#6baed6"
    elif abs_margin < 30:
        category = "Stronghold"
        color = "#cb181d" if party == "Republican" else "#3182bd"
    elif abs_margin < 40:
        category = "Dominant"
        color = "#a50f15" if party == "Republican" else "#08519c"
    else:
        category = "Annihilation"
        color = "#67000d" if party == "Republican" else "#08306b"
    
    return {
        "category": category,
        "party": party,
        "code": f"{party_code}_{category.upper()}",
        "color": color
    }

def parse_csv(path):
    agg = {}
    line_count = 0
    rep_count = 0
    contest_names = set()
    all_parties = set()  # Track all party values
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Strip whitespace from column names
        reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
        print(f"    Columns: {reader.fieldnames}")
        
        for row in reader:
            line_count += 1
            # Try different possible column names
            county = (row.get("COUNTY") or row.get("county") or "").strip().upper()
            contest = (row.get("OFFICENAME") or row.get("office") or row.get("contest") or "").strip().upper()
            party = (row.get("PARTY") or row.get("party") or "").strip().upper()
            candidate = (row.get("CANDIDATE") or row.get("candidate") or "").strip()
            
            # Track all party values we encounter
            if party:
                all_parties.add(party)            # Normalize contest name for consistency across years
            normalized_contest = normalize_contest_name(contest)
            
            # Track contest names
            if contest:
                contest_names.add(f"{contest} -> {normalized_contest}")
            
            try:
                votes = int(float(row.get("VOTES") or row.get("votes") or 0))
            except Exception:
                votes = 0
            
            # Track Republican presidential entries
            if normalized_contest == "PRESIDENT" and (party in ["REPUBLICAN", "REP", "R"] or party.startswith("REP")):
                rep_count += 1
            
            if not county or not contest or votes == 0:
                continue
                
            key = (county, normalized_contest)
            if key not in agg:
                agg[key] = {
                    "dem_votes": 0, "rep_votes": 0, "other_votes": 0, "total_votes": 0,
                    "dem_candidates": {}, "rep_candidates": {}, "other_candidates": {}
                }
            
            # Improved party detection
            if party in ["DEMOCRATIC", "DEM", "D"] or party.startswith("DEM"):
                agg[key]["dem_votes"] += votes
                if candidate:
                    agg[key]["dem_candidates"][candidate] = agg[key]["dem_candidates"].get(candidate, 0) + votes
            elif party in ["REPUBLICAN", "REP", "R"] or party.startswith("REP"):
                agg[key]["rep_votes"] += votes
                if candidate:
                    agg[key]["rep_candidates"][candidate] = agg[key]["rep_candidates"].get(candidate, 0) + votes
            else:
                # Handle cases where party is empty (amendments) or Independent/other
                agg[key]["other_votes"] += votes
                if candidate:
                    agg[key]["other_candidates"][candidate] = agg[key]["other_candidates"].get(candidate, 0) + votes
            
            agg[key]["total_votes"] += votes
    
    # Convert candidate dictionaries to top candidate names
    final_agg = {}
    for key, data in agg.items():
        # Get top candidate for each party
        dem_candidate = max(data["dem_candidates"].items(), key=lambda x: x[1])[0] if data["dem_candidates"] else ""
        rep_candidate = max(data["rep_candidates"].items(), key=lambda x: x[1])[0] if data["rep_candidates"] else ""
        
        # Clean up 2024 presidential candidate names
        if "Electors for Kamala D. Harris for President" in dem_candidate:
            dem_candidate = "Kamala D. Harris"
        if "Electors for Donald J. Trump for President" in rep_candidate:
            rep_candidate = "Donald J. Trump"
        
        final_agg[key] = {
            "dem_votes": data["dem_votes"],
            "rep_votes": data["rep_votes"], 
            "other_votes": data["other_votes"],
            "total_votes": data["total_votes"],
            "dem_candidate": dem_candidate,
            "rep_candidate": rep_candidate
        }
    
    print(f"  Processed {line_count} lines, found {rep_count} Republican entries")
    print(f"  Contest names found: {sorted(list(contest_names))}")
    print(f"  All parties found: {sorted(list(all_parties))}")
    return final_agg

def main():
    results_by_year = {}
    all_contests = set()
    all_precinct_results = 0
    years_covered = set()
    
    print(f"Processing {len(CSV_FILES)} CSV files...")
    for csvfile in CSV_FILES:
        print(f"Processing: {os.path.basename(csvfile)}")
        
        # Check if file exists
        if not os.path.exists(csvfile):
            print(f"  ERROR: File not found - {csvfile}")
            continue
            
        year = extract_year_from_filename(csvfile)
        if not year:
            print(f"  ERROR: Year not found in filename - {csvfile}")
            continue
            
        print(f"  Extracted year: {year}")
        years_covered.add(year)
        
        try:
            agg = parse_csv(csvfile)
            print(f"  Found {len(agg)} county-contest combinations")
        except Exception as e:
            print(f"  ERROR parsing {csvfile}: {e}")
            continue
        for (county, contest), vals in agg.items():
            ctype = contest_type_from_name(contest)
            margin = vals["dem_votes"] - vals["rep_votes"]
            two_party = vals["dem_votes"] + vals["rep_votes"]
            margin_pct = (margin * 100 / two_party) if two_party else 0.0
            
            # Get competitiveness category
            competitiveness = get_competitiveness_category(margin_pct)
            
            # Determine winner
            if vals["dem_votes"] > vals["rep_votes"]:
                winner = "DEM"
            elif vals["rep_votes"] > vals["dem_votes"]:
                winner = "REP"
            else:
                winner = "TIE"
            
            # Create all_parties dict with actual party data
            all_parties = {}
            if vals["dem_votes"] > 0:
                all_parties["DEM"] = vals["dem_votes"]
            if vals["rep_votes"] > 0:
                all_parties["REP"] = vals["rep_votes"]
            if vals["other_votes"] > 0:
                all_parties["OTHER"] = vals["other_votes"]
            
            entry = {
                "county": county,
                "contest": get_display_contest_name(contest),
                "year": year,
                "dem_candidate": vals["dem_candidate"],
                "rep_candidate": vals["rep_candidate"],
                "dem_votes": vals["dem_votes"],
                "rep_votes": vals["rep_votes"],
                "other_votes": vals["other_votes"],
                "total_votes": vals["total_votes"],
                "two_party_total": two_party,
                "margin": abs(margin),
                "margin_pct": abs(margin_pct),
                "winner": winner,
                "competitiveness": competitiveness,
                "all_parties": all_parties,
                "contest_type": ctype
            }
            
            # Create simple county key (just the county name since contest/year are already in the structure)
            county_key = county.replace(" ", "_").replace("/", "_")
            
            # Initialize nested structure using contest name instead of contest type
            if year not in results_by_year:
                results_by_year[year] = {}
            
            # Use normalized contest name as the top-level key (like NC structure)
            contest_key = contest.lower().replace(" ", "_").replace("&", "and")
            
            if contest_key not in results_by_year[year]:
                results_by_year[year][contest_key] = {}
            
            # Find existing contest or create new one
            contest_id = None
            for existing_id, existing_data in results_by_year[year][contest_key].items():
                if existing_data["contest_name"] == contest:
                    contest_id = existing_id
                    break
            
            if contest_id is None:
                # Create new contest ID
                contest_num = len(results_by_year[year][contest_key]) + 1
                contest_id = f"{contest_key}_{year}_{contest_num}"
                results_by_year[year][contest_key][contest_id] = {
                    "contest_name": contest,
                    "results": {}
                }
            
            results_by_year[year][contest_key][contest_id]["results"][county_key] = entry
            all_contests.add(contest)
            all_precinct_results += 1
    summary = {
        "total_years": len(years_covered),
        "total_contests": len(all_contests),
        "total_precinct_results": all_precinct_results,
        "years_covered": sorted(years_covered)
    }
    
    print(f"\nSummary:")
    print(f"  Years covered: {sorted(years_covered)}")
    print(f"  Total years: {len(years_covered)}")
    print(f"  Total contests: {len(all_contests)}")
    print(f"  Total results: {all_precinct_results}")
    
    # Sort results by year chronologically
    sorted_results_by_year = {}
    for year in sorted(years_covered):
        if year in results_by_year:
            sorted_results_by_year[year] = results_by_year[year]
    
    output = {
        "categorization_system": CATEGORIZATION_SYSTEM,
        "summary": summary,
        "results_by_year": sorted_results_by_year
    }
    with open("all_county_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Wrote all_county_results.json in requested format.")

if __name__ == "__main__":
    main()
