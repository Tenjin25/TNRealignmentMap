import json
import csv
import os

def merge_csv_to_json(json_path, csv_path, output_path, missing_year):
    # ...existing code...
    # Load FIPS mapping for TN counties and build valid county set
    fips_path = "tn_county_fips.csv"
    fips_to_county = {}
    county_to_fips = {}
    valid_counties = set()
    if os.path.exists(fips_path):
        with open(fips_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fips = row["FIPS"].zfill(3)
                county = row["COUNTY"].strip()
                fips_to_county[fips] = county
                county_to_fips[county.lower()] = fips
                valid_counties.add(county.lower())
        print(f"Valid counties from FIPS: {sorted(list(valid_counties))}")
    # Load existing JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Parse CSV
    counties = {}
    aggregation = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        county_col = None
        for col in header:
            if col.strip().lower() == "county":
                county_col = col
        contest_col = None
        for col in header:
            if col.strip().lower() in ["officename", "office", "contest", "race", "seat"]:
                contest_col = col
                break
        for row in reader:
            raw_county = row.get(county_col, "").strip()
            print(f"Raw county from CSV: '{raw_county}'")
            # Use raw county name (title-cased and stripped) if it matches valid_counties
            norm_county = raw_county.strip().lower()
            if norm_county in valid_counties:
                county = raw_county.strip().title()
            else:
                # Try FIPS mapping if available
                fips_val = raw_county[-3:] if raw_county else None
                county = fips_to_county.get(fips_val, None)
                if county:
                    county = county.strip().title()
            if not county:
                continue  # skip if county not found
            contest = row["CANDIDATE_GROUP"].strip() if "CANDIDATE_GROUP" in row else row[contest_col].strip()
            key = (county, contest)
            if key not in aggregation:
                aggregation[key] = {
                    "dem_votes": 0,
                    "rep_votes": 0,
                    "other_votes": 0,
                    "total_votes": 0,
                    "two_party_total": 0,
                    "margin": 0,
                    "margin_pct": 0.0,
                    "winner": "",
                    "all_parties": {},
                    "candidates": {},
                    "competitiveness_category": "",
                    "competitiveness_color": "",
                    "party": "",
                    "competitiveness_winner": ""
                }
            # Aggregate votes
            party = row.get("PARTY", row.get("party", "")).strip().upper()
            candidate = row.get("CANDIDATE", row.get("candidate", "")).strip()
            votes = int(row.get("VOTES", row.get("votes", 0))) if str(row.get("VOTES", row.get("votes", "")).strip()).isdigit() else 0
            if candidate:
                if candidate not in aggregation[key]["candidates"]:
                    aggregation[key]["candidates"][candidate] = 0
                aggregation[key]["candidates"][candidate] += votes
            if party:
                if party not in aggregation[key]["all_parties"]:
                    aggregation[key]["all_parties"][party] = 0
                aggregation[key]["all_parties"][party] += votes
            if party in ["D", "DEM"]:
                aggregation[key]["dem_votes"] += votes
            elif party in ["R", "REP"]:
                aggregation[key]["rep_votes"] += votes
            else:
                aggregation[key]["other_votes"] += votes
            aggregation[key]["total_votes"] += votes

    def categorize_competitiveness(winner, margin_pct):
        # Republican scale
        if winner == "REP":
            if margin_pct >= 40:
                return {"category": "Annihilation", "party": "Republican", "code": "R_ANNIHILATION", "color": "#67000d"}
            elif margin_pct >= 30:
                return {"category": "Dominant", "party": "Republican", "code": "R_DOMINANT", "color": "#a50f15"}
            elif margin_pct >= 20:
                return {"category": "Stronghold", "party": "Republican", "code": "R_STRONGHOLD", "color": "#cb181d"}
            elif margin_pct >= 10:
                return {"category": "Safe", "party": "Republican", "code": "R_SAFE", "color": "#ef3b2c"}
            elif margin_pct >= 5.5:
                return {"category": "Likely", "party": "Republican", "code": "R_LIKELY", "color": "#fb6a4a"}
            elif margin_pct >= 1:
                return {"category": "Lean", "party": "Republican", "code": "R_LEAN", "color": "#fcae91"}
            elif margin_pct >= 0.5:
                return {"category": "Tilt", "party": "Republican", "code": "R_TILT", "color": "#fee8c8"}
        # Democratic scale
        elif winner == "DEM":
            if margin_pct >= 40:
                return {"category": "Annihilation", "party": "Democratic", "code": "D_ANNIHILATION", "color": "#08306b"}
            elif margin_pct >= 30:
                return {"category": "Dominant", "party": "Democratic", "code": "D_DOMINANT", "color": "#08519c"}
            elif margin_pct >= 20:
                return {"category": "Stronghold", "party": "Democratic", "code": "D_STRONGHOLD", "color": "#3182bd"}
            elif margin_pct >= 10:
                return {"category": "Safe", "party": "Democratic", "code": "D_SAFE", "color": "#6baed6"}
            elif margin_pct >= 5.5:
                return {"category": "Likely", "party": "Democratic", "code": "D_LIKELY", "color": "#9ecae1"}
            elif margin_pct >= 1:
                return {"category": "Lean", "party": "Democratic", "code": "D_LEAN", "color": "#c6dbef"}
            elif margin_pct >= 0.5:
                return {"category": "Tilt", "party": "Democratic", "code": "D_TILT", "color": "#e1f5fe"}
        # Tossup
        if abs(margin_pct) < 0.5:
            return {"category": "Tossup", "party": "Tossup", "code": "TOSSUP", "color": "#f7f7f7"}
        return {"category": "", "party": "", "code": "", "color": ""}

    # Aggregate results into counties dict
    for (county, contest), result in aggregation.items():
        result["two_party_total"] = result["dem_votes"] + result["rep_votes"]
        result["margin"] = abs(result["dem_votes"] - result["rep_votes"])
        if result["two_party_total"] > 0:
            result["margin_pct"] = round(result["margin"] / result["two_party_total"] * 100, 2)
            if result["dem_votes"] > result["rep_votes"]:
                result["winner"] = "DEM"
                result["party"] = "DEM"
            elif result["rep_votes"] > result["dem_votes"]:
                result["winner"] = "REP"
                result["party"] = "REP"
            else:
                result["winner"] = "TIE"
                result["party"] = "TIE"
        else:
            result["margin_pct"] = 0.0
            result["winner"] = ""
            result["party"] = ""
        # Use new competitiveness categorization system
        comp = categorize_competitiveness(result["winner"], result["margin_pct"])
        result["competitiveness"] = comp
        result["competitiveness_category"] = comp["category"]
        result["competitiveness_color"] = comp["color"]
        result["competitiveness_winner"] = result["winner"]
        # Fill candidates and parties if present
        if result["candidates"]:
            max_votes = max(result["candidates"].values())
            winners = [cand for cand, votes in result["candidates"].items() if votes == max_votes]
            if len(winners) == 1:
                result["winner"] = winners[0]
        if result["all_parties"]:
            max_party_votes = max(result["all_parties"].values())
            winning_parties = [party for party, votes in result["all_parties"].items() if votes == max_party_votes]
            if len(winning_parties) == 1:
                result["party"] = winning_parties[0]
        # Add dem_candidate and rep_candidate fields
        dem_candidate = None
        rep_candidate = None
        # Try to infer from candidates and all_parties
        if result["candidates"] and result["all_parties"]:
            dem_votes = result["all_parties"].get("DEM", result["all_parties"].get("D", 0))
            rep_votes = result["all_parties"].get("REP", result["all_parties"].get("R", 0))
            for cand, votes in result["candidates"].items():
                if votes == dem_votes and dem_votes > 0:
                    dem_candidate = cand
                if votes == rep_votes and rep_votes > 0:
                    rep_candidate = cand
        result["dem_candidate"] = dem_candidate if dem_candidate else ""
        result["rep_candidate"] = rep_candidate if rep_candidate else ""
        if county not in counties:
            counties[county] = {}
        counties[county][contest] = result
    # Insert into JSON structure
    if "results" not in data:
        print("Error: 'results' key not found in JSON.")
        return
    data["results"][missing_year] = counties
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Merged {len(counties)} counties for {missing_year} into {output_path}")

if __name__ == "__main__":
    # Paths for each year
    json_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json"
    output_path = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"
    years_and_csvs = [
        ("2004", ["Election_Data/standardized/2004_standardized_long.csv"]),
        ("2006", [
            "Election_Data/standardized/2006_standardized_governor_long.csv",
            "Election_Data/standardized/2006_standardized_senate_long.csv"
        ])
    ] + [
        (str(year), [f"Election_Data/standardized/{year}_standardized_long.csv"]) for year in range(2007, 2025)
    ]
    # Merge each year in sequence, updating output each time
    current_json = json_path
    import os
    for year, csv_files in years_and_csvs:
        valid_csvs = [csv for csv in csv_files if os.path.exists(csv)]
        if not valid_csvs:
            print(f"Skipping {year}: no valid CSV files found.")
            continue
        # For years with multiple CSVs, merge them sequentially
        for csv_file in valid_csvs:
            merge_csv_to_json(current_json, csv_file, output_path, year)
            current_json = output_path
