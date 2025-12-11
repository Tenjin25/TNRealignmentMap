#!/usr/bin/env python3
"""
Fix color assignments in JSON data to match precise margin percentages.

This script corrects the competitiveness colors and categories in the JSON
to match the exact margin ranges.
"""

import json
from collections import defaultdict

def get_competitiveness_info(margin_pct, winner):
    """Get competitiveness category, color, and description based on margin percentage and winner"""
    if margin_pct >= 40.00:
        category = "Annihilation"
        color = "#67000d" if winner == "Republican" else "#08306b"
        range_desc = "40%+"
    elif 30.00 <= margin_pct < 40.00:
        category = "Dominant"
        color = "#a50f15" if winner == "Republican" else "#08519c"
        range_desc = "30-40%"
    elif 20.00 <= margin_pct < 30.00:
        category = "Stronghold"
        color = "#cb181d" if winner == "Republican" else "#3182bd"
        range_desc = "20-30%"
    elif 10.00 <= margin_pct < 20.00:
        category = "Safe"
        color = "#ef3b2c" if winner == "Republican" else "#6baed6"
        range_desc = "10-20%"
    elif 5.50 <= margin_pct < 10.00:
        category = "Likely"
        color = "#fb6a4a" if winner == "Republican" else "#9ecae1"
        range_desc = "5.5-10%"
    elif 1.00 <= margin_pct < 5.50:
        category = "Lean"
        color = "#fcae91" if winner == "Republican" else "#c6dbef"
        range_desc = "1-5.5%"
    elif 0.50 <= margin_pct < 1.00:
        category = "Tilt"
        color = "#fee8c8" if winner == "Republican" else "#e1f5fe"
        range_desc = "0.5-1%"
    else:
        category = "Tossup"
        color = "#f7f7f7"
        range_desc = "±0.5%"
        winner = None  # Tossup has no party
    
    # Build description
    if winner:
        description = f"{category} {winner}"
        code = f"{winner.upper()[:3]}_{category.upper()}"
    else:
        description = "Tossup"
        code = "TOSSUP"
    
    return {
        "category": category,
        "party": winner,
        "code": code,
        "color": color,
        "description": description
    }

def fix_json_colors(json_path, output_path=None):
    """Fix color assignments in JSON data"""
    print("=" * 80)
    print("Fixing JSON Color Assignments")
    print("=" * 80)
    print()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    corrections = 0
    total_checked = 0
    
    # Fix each year's data
    results_by_year = data.get('results_by_year', {})
    
    for year_num, year_data in results_by_year.items():
        for contest_type, contest_data_dict in year_data.items():
            for contest_id, contest in contest_data_dict.items():
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
                    
                    # Get current competitiveness
                    current_comp = county_data.get('competitiveness', {})
                    current_color = current_comp.get('color', '').lower()
                    
                    # Get correct competitiveness info
                    correct_comp = get_competitiveness_info(margin_pct, winner)
                    
                    # Check if correction is needed
                    if current_color != correct_comp['color'].lower():
                        corrections += 1
                        # Update the competitiveness field
                        county_data['competitiveness'] = correct_comp
    
    # Save corrected JSON
    if output_path is None:
        output_path = json_path.replace('.json', '_corrected.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Report results
    print(f"Total county-contest combinations checked: {total_checked}")
    print(f"Corrections made: {corrections}")
    print(f"\n✓ Corrected JSON saved to: {output_path}")
    
    if corrections > 0:
        print(f"\n{corrections} colors were corrected to match precise margin ranges:")
        print("  - Tilt: 0.50-0.99%")
        print("  - Lean: 1.00-5.49%")
        print("  - Likely: 5.50-9.99%")
        print("  - Safe: 10.00-19.99%")
        print("  - Stronghold: 20.00-29.99%")
        print("  - Dominant: 30.00-39.99%")
        print("  - Annihilation: >= 40.00%")
    else:
        print("\n✓ No corrections needed - all colors already accurate!")
    
    print()

if __name__ == "__main__":
    json_path = "all_county_results.json"
    fix_json_colors(json_path)
