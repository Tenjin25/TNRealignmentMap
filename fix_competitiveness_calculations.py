#!/usr/bin/env python3

import json

def get_competitiveness(margin_pct, winning_party):
    """Calculate competitiveness category based on margin percentage and winning party"""
    abs_margin = abs(margin_pct)
    
    # Define the ranges based on your categorization system
    if abs_margin < 0.5:
        return "Tossup", "#f7f7f7"
    elif abs_margin < 1:
        category = "Tilt"
    elif abs_margin < 5.5:
        category = "Lean"
    elif abs_margin < 10:
        category = "Likely"
    elif abs_margin < 20:
        category = "Safe"
    elif abs_margin < 30:
        category = "Stronghold"
    elif abs_margin < 40:
        category = "Dominant"
    else:
        category = "Annihilation"
    
    # Get the appropriate color based on party and category
    if winning_party == 'Republican':
        colors = {
            'Tilt': '#fee8c8',
            'Lean': '#fcae91',
            'Likely': '#fb6a4a',
            'Safe': '#ef3b2c',
            'Stronghold': '#cb181d',
            'Dominant': '#a50f15',
            'Annihilation': '#67000d'
        }
    elif winning_party == 'Democratic':
        colors = {
            'Tilt': '#e1f5fe',
            'Lean': '#c6dbef',
            'Likely': '#9ecae1',
            'Safe': '#6baed6',
            'Stronghold': '#3182bd',
            'Dominant': '#08519c',
            'Annihilation': '#08306b'
        }
    else:
        return "Tossup", "#f7f7f7"
    
    return category, colors[category]

def fix_competitiveness_calculations():
    """Fix competitiveness calculations based on actual county vote margins"""
    
    # Load the data
    with open('all_county_results.json', 'r') as f:
        data = json.load(f)
    
    contests_fixed = 0
    counties_fixed = 0
    
    # Check all years and contest types
    for year in data['results_by_year']:
        for contest_type in data['results_by_year'][year]:
            for contest_id in data['results_by_year'][year][contest_type]:
                contest = data['results_by_year'][year][contest_type][contest_id]
                
                # Skip if no results
                if 'results' not in contest:
                    continue
                
                print(f"Fixing {year} {contest_type} {contest_id}...")
                contests_fixed += 1
                
                for county_name, county_data in contest['results'].items():
                    # Calculate the actual margin based on county vote totals
                    dem_votes = county_data.get('dem_votes', 0)
                    rep_votes = county_data.get('rep_votes', 0)
                    total_votes = county_data.get('total_votes', 0)
                    
                    if dem_votes + rep_votes == 0:
                        continue
                        
                    # Calculate two-party total and margin
                    two_party_total = dem_votes + rep_votes
                    margin = rep_votes - dem_votes  # Positive = Republican lead
                    margin_pct = (margin / two_party_total) * 100 if two_party_total > 0 else 0
                    
                    # Determine winner and winning party
                    if rep_votes > dem_votes:
                        winner = 'REP'
                        winning_party = 'Republican'
                    elif dem_votes > rep_votes:
                        winner = 'DEM'
                        winning_party = 'Democratic'
                    else:
                        winner = 'TIE'
                        winning_party = 'Tie'
                    
                    # Get competitiveness category and color
                    if winning_party == 'Tie':
                        category = 'Tossup'
                        code = 'TIE'
                        color = '#f7f7f7'
                    else:
                        category, color = get_competitiveness(margin_pct, winning_party)
                        party_code = 'DEM' if winning_party == 'Democratic' else 'REP'
                        code = f"{party_code}_{category.upper()}"
                    
                    # Update the county data
                    county_data['margin'] = abs(margin)
                    county_data['margin_pct'] = abs(margin_pct)
                    county_data['two_party_total'] = two_party_total
                    county_data['winner'] = winner
                    county_data['competitiveness'] = {
                        'category': category,
                        'party': winning_party,
                        'code': code,
                        'color': color
                    }
                    
                    counties_fixed += 1
    
    # Save the corrected data
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed competitiveness calculations for {contests_fixed} contests and {counties_fixed} counties")
    
    # Show some sample results
    print("\nSample corrected results for 2006 Senate:")
    contest = data['results_by_year']['2006']['us_senate']['us_senate_2006_1']['results']
    sample_counties = ['DAVIDSON', 'SHELBY', 'HAMILTON', 'KNOX', 'ANDERSON']
    
    for county in sample_counties:
        if county in contest:
            result = contest[county]
            comp = result['competitiveness']
            print(f"{county}: {result['margin_pct']:.1f}% {comp['party']} {comp['category']} ({comp['color']})")

if __name__ == "__main__":
    fix_competitiveness_calculations()