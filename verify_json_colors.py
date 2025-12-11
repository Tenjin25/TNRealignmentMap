#!/usr/bin/env python3
"""
Verify that color assignments in JSON data match margin percentages.

This script checks if the competitiveness colors assigned in the JSON
match the expected colors based on the actual margin percentages.
"""

import json
from collections import defaultdict

# Expected color mapping based on margins
def get_expected_color(margin_pct, winner):
    """Get expected color based on margin percentage and winner"""
    if margin_pct >= 40.00:
        return "#67000d" if winner == "Republican" else "#08306b"  # Annihilation (>= 40)
    elif 30.00 <= margin_pct < 40.00:
        return "#a50f15" if winner == "Republican" else "#08519c"  # Dominant (30-39.99)
    elif 20.00 <= margin_pct < 30.00:
        return "#cb181d" if winner == "Republican" else "#3182bd"  # Stronghold (20-29.99)
    elif 10.00 <= margin_pct < 20.00:
        return "#ef3b2c" if winner == "Republican" else "#6baed6"  # Safe (10-19.99)
    elif 5.50 <= margin_pct < 10.00:
        return "#fb6a4a" if winner == "Republican" else "#9ecae1"  # Likely (5.50-9.99)
    elif 1.00 <= margin_pct < 5.50:
        return "#fcae91" if winner == "Republican" else "#c6dbef"  # Lean (1-5.49)
    elif 0.50 <= margin_pct < 1.00:
        return "#fee8c8" if winner == "Republican" else "#e1f5fe"  # Tilt (0.50-0.99)
    else:
        return "#f7f7f7"  # Tossup (< 0.50)

def verify_json_colors(json_path):
    """Verify color assignments in JSON data"""
    print("=" * 80)
    print("JSON Color Verification - Checking margin vs color accuracy")
    print("=" * 80)
    print()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mismatches = []
    total_checked = 0
    years_with_issues = defaultdict(list)
    
    # Check each year's data - actual structure is results_by_year
    results_by_year = data.get('results_by_year', {})
    
    for year_num, year_data in results_by_year.items():
        for contest_type, contest_data_dict in year_data.items():
            for contest_id, contest in contest_data_dict.items():
                contest_name = contest.get('contest_name', 'Unknown')
                results = contest.get('results', {})
                
                for county, county_data in results.items():
                    total_checked += 1
                    
                    # Get votes
                    dem_votes = county_data.get('dem_votes', 0)
                    rep_votes = county_data.get('rep_votes', 0)
                    total_votes = county_data.get('total_votes', 0)
                    
                    if total_votes == 0:
                        continue
                    
                    # Calculate margin
                    dem_pct = (dem_votes / total_votes) * 100
                    rep_pct = (rep_votes / total_votes) * 100
                    margin_pct = abs(rep_pct - dem_pct)
                    winner = "Republican" if rep_pct > dem_pct else "Democratic"
                    
                    # Get assigned color from JSON
                    comp_data = county_data.get('competitiveness', {})
                    assigned_color = comp_data.get('color', '').lower()
                    
                    # Get expected color
                    expected_color = get_expected_color(margin_pct, winner).lower()
                    
                    # Check if they match
                    if assigned_color and assigned_color != expected_color:
                        mismatch = {
                            'year': year_num,
                            'contest': contest_name,
                            'county': county,
                            'margin': f"{margin_pct:.2f}%",
                            'winner': winner,
                            'expected_color': expected_color,
                            'assigned_color': assigned_color,
                            'description': comp_data.get('description', 'Unknown')
                        }
                        mismatches.append(mismatch)
                        years_with_issues[year_num].append(mismatch)
    
    # Report results
    print(f"Total county-contest combinations checked: {total_checked}")
    print(f"Mismatches found: {len(mismatches)}")
    print()
    
    if mismatches:
        print("COLOR MISMATCHES DETECTED")
        print("-" * 80)
        
        # Show first 20 mismatches
        for i, m in enumerate(mismatches[:20]):
            print(f"\n{i+1}. {m['year']} - {m['contest']} - {m['county']}")
            print(f"   Margin: {m['winner']} +{m['margin']}")
            print(f"   Expected: {m['expected_color']}")
            print(f"   Assigned: {m['assigned_color']}")
            print(f"   Category: {m['description']}")
        
        if len(mismatches) > 20:
            print(f"\n... and {len(mismatches) - 20} more mismatches")
        
        print("\n" + "=" * 80)
        print("YEARS WITH ISSUES")
        print("=" * 80)
        for year in sorted(years_with_issues.keys()):
            print(f"  {year}: {len(years_with_issues[year])} mismatches")
    else:
        print("✓ ALL COLOR ASSIGNMENTS ARE ACCURATE!")
        print("  All colors match the expected values based on margin percentages.")
    
    print()

if __name__ == "__main__":
    import sys
    json_path = sys.argv[1] if len(sys.argv) > 1 else "all_county_results.json"
    verify_json_colors(json_path)
