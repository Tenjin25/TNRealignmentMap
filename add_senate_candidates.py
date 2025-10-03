#!/usr/bin/env python3
"""
Add candidate names and formatting to remaining US Senate races
"""

import json

def calculate_competitiveness_description(category, party):
    """Convert category/party to simplified description like Senate races"""
    if party == 'Democratic':
        if category == 'Annihilation':
            return 'Annihilation Democratic'
        elif category == 'Dominant':
            return 'Dominant Democratic'
        elif category == 'Stronghold':
            return 'Stronghold Democratic'
        elif category == 'Safe':
            return 'Safe Democratic'
        elif category == 'Likely':
            return 'Likely Democratic'
        elif category == 'Lean':
            return 'Lean Democratic'
        elif category == 'Tilt':
            return 'Tilt Democratic'
    elif category == 'Republican':
        if category == 'Annihilation':
            return 'Annihilation Republican'
        elif category == 'Dominant':
            return 'Dominant Republican'
        elif category == 'Stronghold':
            return 'Stronghold Republican'
        elif category == 'Safe':
            return 'Safe Republican'
        elif category == 'Likely':
            return 'Likely Republican'
        elif category == 'Lean':
            return 'Lean Republican'
        elif category == 'Tilt':
            return 'Tilt Republican'
    return f"{category} {party}"

def get_senate_candidates(year):
    """Get known Senate candidate names"""
    candidates = {
        '2008': {'dem': 'Bob Tuke', 'rep': 'Lamar Alexander'},
        '2012': {'dem': 'Mark Clayton', 'rep': 'Bob Corker'},
        '2018': {'dem': 'Phil Bredesen', 'rep': 'Marsha Blackburn'},
        '2020': {'dem': 'Marquita Bradshaw', 'rep': 'Bill Hagerty'},
        '2024': {'dem': 'Gloria Johnson', 'rep': 'Marsha Blackburn'},
    }
    
    if year in candidates:
        return candidates[year]
    return {'dem': None, 'rep': None}

def update_senate_races():
    """Update remaining Senate races with proper formatting"""
    
    # Load the data
    with open('all_county_results.json', 'r') as f:
        data = json.load(f)
    
    races_updated = 0
    
    # Process Senate races that need updates
    for year, year_data in data['results_by_year'].items():
        if 'us_senate' in year_data:
            for contest_id, contest_data in year_data['us_senate'].items():
                
                # Check if this race needs updates (missing candidates)
                if not contest_data.get('dem_candidate') or not contest_data.get('rep_candidate'):
                    
                    # Update contest name
                    contest_data['contest_name'] = f'{year} US Senate'
                    
                    # Add candidate names
                    candidates = get_senate_candidates(year)
                    if candidates['dem']:
                        contest_data['dem_candidate'] = candidates['dem']
                    if candidates['rep']:
                        contest_data['rep_candidate'] = candidates['rep']
                    
                    # Update competitiveness descriptions for all counties if needed
                    for county_name, county_data in contest_data['results'].items():
                        if 'competitiveness' in county_data:
                            comp = county_data['competitiveness']
                            if 'category' in comp and 'party' in comp and 'description' not in comp:
                                # Add the simplified description field
                                comp['description'] = calculate_competitiveness_description(
                                    comp['category'], comp['party']
                                )
                    
                    races_updated += 1
                    print(f"Updated Senate {year}: {candidates['dem']} vs {candidates['rep']}")
    
    # Save the updated data
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSuccessfully updated {races_updated} Senate races!")

if __name__ == '__main__':
    update_senate_races()