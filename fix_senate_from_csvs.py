#!/usr/bin/env python3

import json
import pandas as pd

def load_2006_senate_from_csv():
    """Load 2006 Senate data from standardized CSV"""
    df = pd.read_csv('Election_Data/standardized/2006_standardized_senate_long.csv')
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Filter for just the U.S. Senate race
    senate_df = df[df['office'].str.contains('Senate', case=False, na=False)]
    
    # Group by county and candidate to get county totals
    county_totals = senate_df.groupby(['county', 'candidate', 'party'])['votes'].sum().reset_index()
    
    # Create county-level results dictionary
    results = {}
    
    for county in county_totals['county'].unique():
        county_data = county_totals[county_totals['county'] == county]
        
        # Get votes by party
        dem_votes = county_data[county_data['party'] == 'D']['votes'].sum()
        rep_votes = county_data[county_data['party'] == 'R']['votes'].sum()
        other_votes = county_data[~county_data['party'].isin(['D', 'R'])]['votes'].sum()
        
        # Get candidate names
        dem_candidate = county_data[county_data['party'] == 'D']['candidate'].iloc[0] if len(county_data[county_data['party'] == 'D']) > 0 else 'Harold Ford Jr.'
        rep_candidate = county_data[county_data['party'] == 'R']['candidate'].iloc[0] if len(county_data[county_data['party'] == 'R']) > 0 else 'Bob Corker'
        
        results[county.upper()] = {
            'dem_votes': int(dem_votes),
            'rep_votes': int(rep_votes),
            'other_votes': int(other_votes),
            'dem_candidate': dem_candidate.strip('"'),
            'rep_candidate': rep_candidate
        }
    
    return results

def load_2014_senate_from_csv():
    """Load 2014 Senate data from standardized CSV"""
    df = pd.read_csv('Election_Data/standardized/2014_standardized_long.csv')
    
    # Strip whitespace from column names  
    df.columns = df.columns.str.strip()
    
    # Filter for U.S. Senator race
    senate_df = df[df['OFFICENAME'].str.contains('United States Senate|U.S. Senator|US Senator', case=False, na=False)]
    
    if len(senate_df) == 0:
        print("No U.S. Senator entries found, checking all office names...")
        print("Available offices:", df['OFFICENAME'].unique()[:10])
        return {}
    
    # Group by county and candidate
    county_totals = senate_df.groupby(['COUNTY', 'CANDIDATE', 'PARTY'])['VOTES'].sum().reset_index()
    
    results = {}
    
    for county in county_totals['COUNTY'].unique():
        county_data = county_totals[county_totals['COUNTY'] == county]
        
        # Get votes by party
        dem_votes = county_data[county_data['PARTY'].str.contains('Democratic', case=False, na=False)]['VOTES'].sum()
        rep_votes = county_data[county_data['PARTY'].str.contains('Republican', case=False, na=False)]['VOTES'].sum()
        other_votes = county_data[~county_data['PARTY'].str.contains('Democratic|Republican', case=False, na=False)]['VOTES'].sum()
        
        # Get candidate names
        dem_candidates = county_data[county_data['PARTY'].str.contains('Democratic', case=False, na=False)]['CANDIDATE']
        rep_candidates = county_data[county_data['PARTY'].str.contains('Republican', case=False, na=False)]['CANDIDATE']
        
        dem_candidate = dem_candidates.iloc[0].strip('"') if len(dem_candidates) > 0 else 'Gordon Ball'
        rep_candidate = rep_candidates.iloc[0] if len(rep_candidates) > 0 else 'Lamar Alexander'
        
        results[county.upper()] = {
            'dem_votes': int(dem_votes),
            'rep_votes': int(rep_votes), 
            'other_votes': int(other_votes),
            'dem_candidate': dem_candidate,
            'rep_candidate': rep_candidate
        }
    
    return results

def calculate_competitiveness(dem_votes, rep_votes):
    """Calculate competitiveness category and color"""
    total = dem_votes + rep_votes
    if total == 0:
        return 'Tossup', 'Tie', 'TIE', '#f7f7f7', 'TIE', 0.0
    
    margin = abs(rep_votes - dem_votes)
    margin_pct = (margin / total) * 100
    
    if rep_votes > dem_votes:
        winner = 'REP'
        party = 'Republican'
        if margin_pct >= 40:
            category, color = 'Annihilation', '#67000d'
        elif margin_pct >= 30:
            category, color = 'Dominant', '#a50f15'
        elif margin_pct >= 20:
            category, color = 'Stronghold', '#cb181d'
        elif margin_pct >= 10:
            category, color = 'Safe', '#ef3b2c'
        elif margin_pct >= 5.5:
            category, color = 'Likely', '#fb6a4a'
        elif margin_pct >= 1:
            category, color = 'Lean', '#fcae91'
        elif margin_pct >= 0.5:
            category, color = 'Tilt', '#fee8c8'
        else:
            category, color = 'Tossup', '#f7f7f7'
    else:
        winner = 'DEM'
        party = 'Democratic'
        if margin_pct >= 40:
            category, color = 'Annihilation', '#08306b'
        elif margin_pct >= 30:
            category, color = 'Dominant', '#08519c'
        elif margin_pct >= 20:
            category, color = 'Stronghold', '#3182bd'
        elif margin_pct >= 10:
            category, color = 'Safe', '#6baed6'
        elif margin_pct >= 5.5:
            category, color = 'Likely', '#9ecae1'
        elif margin_pct >= 1:
            category, color = 'Lean', '#c6dbef'
        elif margin_pct >= 0.5:
            category, color = 'Tilt', '#e1f5fe'
        else:
            category, color = 'Tossup', '#f7f7f7'
    
    code = f"{winner}_{category.upper()}" if winner != 'TIE' else 'TIE'
    
    return category, party, code, color, winner, margin_pct

def update_json_with_csv_data():
    """Update the JSON with real CSV data"""
    
    # Load current JSON
    with open('all_county_results.json', 'r') as f:
        data = json.load(f)
    
    # Load CSV data
    print("Loading 2006 Senate data from CSV...")
    csv_2006 = load_2006_senate_from_csv()
    
    print("Loading 2014 Senate data from CSV...")
    csv_2014 = load_2014_senate_from_csv()
    
    # Update 2006 Senate data
    if csv_2006:
        contest_2006 = data['results_by_year']['2006']['us_senate']['us_senate_2006_1']
        contest_2006['contest_name'] = 'US Senate - Harold Ford Jr. (D) vs Bob Corker (R)'
        contest_2006['dem_candidate'] = 'Harold Ford Jr.'
        contest_2006['rep_candidate'] = 'Bob Corker'
        
        for county_name, county_data in contest_2006['results'].items():
            if county_name in csv_2006:
                csv_data = csv_2006[county_name]
                
                # Update vote totals
                county_data['dem_votes'] = csv_data['dem_votes']
                county_data['rep_votes'] = csv_data['rep_votes']
                county_data['other_votes'] = csv_data['other_votes']
                county_data['total_votes'] = csv_data['dem_votes'] + csv_data['rep_votes'] + csv_data['other_votes']
                county_data['two_party_total'] = csv_data['dem_votes'] + csv_data['rep_votes']
                county_data['margin'] = abs(csv_data['rep_votes'] - csv_data['dem_votes'])
                
                # Update candidates
                county_data['dem_candidate'] = csv_data['dem_candidate']
                county_data['rep_candidate'] = csv_data['rep_candidate']
                
                # Calculate competitiveness
                category, party, code, color, winner, margin_pct = calculate_competitiveness(
                    csv_data['dem_votes'], csv_data['rep_votes']
                )
                
                county_data['margin_pct'] = margin_pct
                county_data['winner'] = winner
                county_data['competitiveness'] = {
                    'category': category,
                    'party': party,
                    'code': code,
                    'color': color
                }
                
                county_data['all_parties'] = {
                    'DEM': csv_data['dem_votes'],
                    'REP': csv_data['rep_votes'],
                    'OTHER': csv_data['other_votes']
                }
        
        print(f"Updated 2006 Senate data for {len(csv_2006)} counties")
    
    # Update 2014 Senate data
    if csv_2014:
        contest_2014 = data['results_by_year']['2014']['us_senate']['us_senate_2014_1']
        contest_2014['contest_name'] = 'US Senate - Gordon Ball (D) vs Lamar Alexander (R)'
        contest_2014['dem_candidate'] = 'Gordon Ball'
        contest_2014['rep_candidate'] = 'Lamar Alexander'
        
        for county_name, county_data in contest_2014['results'].items():
            if county_name in csv_2014:
                csv_data = csv_2014[county_name]
                
                # Update vote totals
                county_data['dem_votes'] = csv_data['dem_votes']
                county_data['rep_votes'] = csv_data['rep_votes']
                county_data['other_votes'] = csv_data['other_votes']
                county_data['total_votes'] = csv_data['dem_votes'] + csv_data['rep_votes'] + csv_data['other_votes']
                county_data['two_party_total'] = csv_data['dem_votes'] + csv_data['rep_votes']
                county_data['margin'] = abs(csv_data['rep_votes'] - csv_data['dem_votes'])
                
                # Update candidates
                county_data['dem_candidate'] = csv_data['dem_candidate']
                county_data['rep_candidate'] = csv_data['rep_candidate']
                
                # Calculate competitiveness
                category, party, code, color, winner, margin_pct = calculate_competitiveness(
                    csv_data['dem_votes'], csv_data['rep_votes']
                )
                
                county_data['margin_pct'] = margin_pct
                county_data['winner'] = winner
                county_data['competitiveness'] = {
                    'category': category,
                    'party': party,
                    'code': code,
                    'color': color
                }
                
                county_data['all_parties'] = {
                    'DEM': csv_data['dem_votes'],
                    'REP': csv_data['rep_votes'],
                    'OTHER': csv_data['other_votes']
                }
        
        print(f"Updated 2014 Senate data for {len(csv_2014)} counties")
    
    # Save updated JSON
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("JSON updated with real CSV data!")
    
    # Show sample results
    if csv_2006:
        print("\nSample 2006 results:")
        contest = data['results_by_year']['2006']['us_senate']['us_senate_2006_1']['results']
        for county in ['DAVIDSON', 'SHELBY', 'KNOX', 'WILLIAMSON'][:3]:
            if county in contest:
                result = contest[county]
                comp = result['competitiveness']
                print(f"{county}: {result['dem_votes']} D, {result['rep_votes']} R -> {comp['party']} {comp['category']} ({comp['color']})")

if __name__ == '__main__':
    update_json_with_csv_data()