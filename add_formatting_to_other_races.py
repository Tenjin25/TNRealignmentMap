#!/usr/bin/env python3
"""
Add proper formatting to Presidential and Governor races to match Senate races
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
    elif party == 'Republican':
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

def get_candidate_names(year, contest_type):
    """Get known candidate names for major races"""
    candidates = {
        'president': {
            '2004': {'dem': 'John Kerry', 'rep': 'George W. Bush'},
            '2008': {'dem': 'Barack Obama', 'rep': 'John McCain'},
            '2012': {'dem': 'Barack Obama', 'rep': 'Mitt Romney'},
            '2016': {'dem': 'Hillary Clinton', 'rep': 'Donald Trump'},
            '2020': {'dem': 'Joe Biden', 'rep': 'Donald Trump'},
            '2024': {'dem': 'Kamala Harris', 'rep': 'Donald Trump'},
        },
        'governor': {
            '2006': {'dem': 'Phil Bredesen', 'rep': 'Jim Bryson'},
            '2010': {'dem': 'Mike McWherter', 'rep': 'Bill Haslam'},
            '2014': {'dem': 'Charlie Brown', 'rep': 'Bill Haslam'},
            '2018': {'dem': 'Karl Dean', 'rep': 'Bill Lee'},
            '2022': {'dem': 'Jason Martin', 'rep': 'Bill Lee'},
        }
    }
    
    if contest_type in candidates and year in candidates[contest_type]:
        return candidates[contest_type][year]
    return {'dem': None, 'rep': None}

def update_contest_formatting():
    """Update all President and Governor races with proper formatting"""
    
    # Load the data
    with open('all_county_results.json', 'r') as f:
        data = json.load(f)
    
    races_updated = 0
    
    # Process each year
    for year, year_data in data['results_by_year'].items():
        for contest_type in ['president', 'governor']:
            if contest_type in year_data:
                for contest_id, contest_data in year_data[contest_type].items():
                    
                    # Update contest name
                    if contest_type == 'president':
                        contest_data['contest_name'] = f'{year} Presidential Election'
                    elif contest_type == 'governor':
                        contest_data['contest_name'] = f'{year} Tennessee Governor'
                    
                    # Add candidate names
                    candidates = get_candidate_names(year, contest_type)
                    if candidates['dem']:
                        contest_data['dem_candidate'] = candidates['dem']
                    if candidates['rep']:
                        contest_data['rep_candidate'] = candidates['rep']
                    
                    # Update competitiveness descriptions for all counties
                    for county_name, county_data in contest_data['results'].items():
                        if 'competitiveness' in county_data:
                            comp = county_data['competitiveness']
                            if 'category' in comp and 'party' in comp:
                                # Add the simplified description field
                                comp['description'] = calculate_competitiveness_description(
                                    comp['category'], comp['party']
                                )
                    
                    races_updated += 1
                    print(f"Updated {contest_type} {year}")
    
    # Save the updated data
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSuccessfully updated {races_updated} races with proper formatting!")

if __name__ == '__main__':
    update_contest_formatting()