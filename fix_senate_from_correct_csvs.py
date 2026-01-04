#!/usr/bin/env python3

import pandas as pd
import json

def calculate_competitiveness(dem_votes, rep_votes):
    """Calculate competitiveness category and color based on vote margin."""
    total_votes = dem_votes + rep_votes
    if total_votes == 0:
        return {'category': 'No Data', 'color': '#cccccc', 'description': 'No voting data available'}
    
    dem_pct = (dem_votes / total_votes) * 100
    rep_pct = (rep_votes / total_votes) * 100
    margin = abs(dem_pct - rep_pct)
    winner = 'D' if dem_votes > rep_votes else 'R'
    
    # Define competitiveness categories with proper political colors
    if margin < 0.5:
        # Tossup (±0.5%) - use party colors for visibility
        category = "Tossup"
        base_color = "#2563eb" if winner == 'D' else "#dc2626"
    elif margin < 1:
        # Tilt (0.5-1%)
        category = "Tilt"
        base_color = "#e1f5fe" if winner == 'D' else "#fee8c8"
    elif margin < 5.5:
        # Lean (1-5.5%)
        category = "Lean"
        base_color = "#c6dbef" if winner == 'D' else "#fcae91"
    elif margin < 10:
        # Likely (5.5-10%)
        category = "Likely"
        base_color = "#9ecae1" if winner == 'D' else "#fb6a4a"
    elif margin < 20:
        # Safe (10-20%)
        category = "Safe"
        base_color = "#6baed6" if winner == 'D' else "#ef3b2c"
    elif margin < 30:
        # Stronghold (20-30%)
        category = "Stronghold"
        base_color = "#3182bd" if winner == 'D' else "#cb181d"
    elif margin < 40:
        # Dominant (30-40%)
        category = "Dominant"
        base_color = "#08519c" if winner == 'D' else "#a50f15"
    else:
        # Annihilation (40%+)
        category = "Annihilation"
        base_color = "#08306b" if winner == 'D' else "#67000d"
    
    # Create proper party name and description
    party_name = "Democratic" if winner == 'D' else "Republican"
    
    # Special handling for tossup format to match Florida map
    if category == "Tossup":
        description = f"Tossup ({party_name} Win)"
    else:
        description = f"{category} {party_name}"
    
    return {
        'category': category,
        'color': base_color,
        'description': description
    }

def load_2006_senate_from_csv():
    """Load 2006 Senate data from the original CSV file."""
    print("Loading 2006 Senate data from CSV...")
    
    # Read the CSV data
    df = pd.read_csv('Election_Data/CSVs/20061107__tn__general__senate__precinct.csv')
    
    # Filter for main candidates
    harold_ford = df[df['candidate'] == 'Harold Ford Jr.'].copy()
    bob_corker = df[df['candidate'] == 'Bob Corker'].copy()
    
    print(f"Found {len(harold_ford)} Harold Ford Jr. records")
    print(f"Found {len(bob_corker)} Bob Corker records")
    
    # Aggregate by county
    harold_county = harold_ford.groupby('county')['votes'].sum()
    corker_county = bob_corker.groupby('county')['votes'].sum()
    
    print(f"Counties in Harold data: {len(harold_county)}")
    print(f"Counties in Corker data: {len(corker_county)}")
    
    # Create results dictionary
    results = {}
    
    all_counties = set(harold_county.index) | set(corker_county.index)
    
    for county in all_counties:
        dem_votes = harold_county.get(county, 0)
        rep_votes = corker_county.get(county, 0)
        
        total_votes = dem_votes + rep_votes
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        margin_pct = abs(dem_pct - rep_pct)
        
        competitiveness = calculate_competitiveness(dem_votes, rep_votes)
        
        results[county.upper()] = {
            'dem_votes': int(dem_votes),
            'rep_votes': int(rep_votes),
            'total_votes': int(total_votes),
            'dem_pct': round(dem_pct, 2),
            'rep_pct': round(rep_pct, 2),
            'margin_pct': round(margin_pct, 2),
            'competitiveness': competitiveness
        }
    
    print(f"Processed {len(results)} counties")
    print("Sample counties:")
    for county in ['DAVIDSON', 'SHELBY', 'KNOX']:
        if county in results:
            r = results[county]
            print(f"  {county}: {r['dem_votes']} D, {r['rep_votes']} R, {r['margin_pct']:.1f}% margin")
    
    return results

def load_2014_senate_from_csv():
    """Load 2014 Senate data from the original CSV file."""
    print("\nLoading 2014 Senate data from CSV...")
    
    # Read the CSV data
    df = pd.read_csv('Election_Data/CSVs/20141104__tn__general__precinct.csv')
    
    print("Available candidates:")
    print(df['candidate'].value_counts())
    
    # Filter for main candidates (need to find the correct names)
    lamar_alexander = df[df['candidate'].str.contains('Lamar Alexander', case=False, na=False)].copy()
    gordon_ball = df[df['candidate'].str.contains('Gordon Ball', case=False, na=False)].copy()
    
    print(f"Found {len(lamar_alexander)} Lamar Alexander records")
    print(f"Found {len(gordon_ball)} Gordon Ball records")
    
    if len(lamar_alexander) == 0 or len(gordon_ball) == 0:
        print("Using exact candidate names...")
        # Try exact matches from the value_counts
        candidates = df['candidate'].unique()
        print("All candidates:", candidates[:10])  # Show first 10
        
        # Find the exact names
        for candidate in candidates:
            if 'Alexander' in candidate:
                lamar_alexander = df[df['candidate'] == candidate].copy()
                print(f"Using Alexander candidate: '{candidate}'")
                break
                
        for candidate in candidates:
            if 'Ball' in candidate:
                gordon_ball = df[df['candidate'] == candidate].copy()
                print(f"Using Ball candidate: '{candidate}'")
                break
    
    # Aggregate by county
    alexander_county = lamar_alexander.groupby('county')['votes'].sum()
    ball_county = gordon_ball.groupby('county')['votes'].sum()
    
    print(f"Counties in Alexander data: {len(alexander_county)}")
    print(f"Counties in Ball data: {len(ball_county)}")
    
    # Create results dictionary
    results = {}
    
    all_counties = set(alexander_county.index) | set(ball_county.index)
    
    for county in all_counties:
        dem_votes = ball_county.get(county, 0)  # Ball is Democrat
        rep_votes = alexander_county.get(county, 0)  # Alexander is Republican
        
        total_votes = dem_votes + rep_votes
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        margin_pct = abs(dem_pct - rep_pct)
        
        competitiveness = calculate_competitiveness(dem_votes, rep_votes)
        
        results[county.upper()] = {
            'dem_votes': int(dem_votes),
            'rep_votes': int(rep_votes),
            'total_votes': int(total_votes),
            'dem_pct': round(dem_pct, 2),
            'rep_pct': round(rep_pct, 2),
            'margin_pct': round(margin_pct, 2),
            'competitiveness': competitiveness
        }
    
    print(f"Processed {len(results)} counties")
    print("Sample counties:")
    for county in ['DAVIDSON', 'SHELBY', 'KNOX']:
        if county in results:
            r = results[county]
            print(f"  {county}: {r['dem_votes']} D, {r['rep_votes']} R, {r['margin_pct']:.1f}% margin")
    
    return results

def main():
    # Load the existing JSON data
    with open('all_county_results.json', 'r') as f:
        data = json.load(f)
    
    # Load 2006 Senate data from CSV
    senate_2006_results = load_2006_senate_from_csv()
    
    # Update 2006 Senate data
    if 'results_by_year' not in data:
        data['results_by_year'] = {}
    if '2006' not in data['results_by_year']:
        data['results_by_year']['2006'] = {}
    if 'us_senate' not in data['results_by_year']['2006']:
        data['results_by_year']['2006']['us_senate'] = {}
    
    data['results_by_year']['2006']['us_senate']['us_senate_2006_1'] = {
        'contest_name': '2006 US Senate - Harold Ford Jr. (D) vs Bob Corker (R)',
        'dem_candidate': 'Harold Ford Jr.',
        'rep_candidate': 'Bob Corker',
        'results': senate_2006_results
    }
    
    # Calculate 2006 statewide totals
    total_2006_dem = sum(r['dem_votes'] for r in senate_2006_results.values())
    total_2006_rep = sum(r['rep_votes'] for r in senate_2006_results.values())
    print(f"\n2006 statewide totals: Harold Ford Jr. (D) {total_2006_dem:,}, Bob Corker (R) {total_2006_rep:,}")
    
    # Try to load 2014 Senate data from CSV
    try:
        senate_2014_results = load_2014_senate_from_csv()
        
        # Update 2014 Senate data
        if '2014' not in data['results_by_year']:
            data['results_by_year']['2014'] = {}
        if 'us_senate' not in data['results_by_year']['2014']:
            data['results_by_year']['2014']['us_senate'] = {}
        
        data['results_by_year']['2014']['us_senate']['us_senate_2014_1'] = {
            'contest_name': '2014 US Senate - Gordon Ball (D) vs Lamar Alexander (R)',
            'dem_candidate': 'Gordon Ball',
            'rep_candidate': 'Lamar Alexander',
            'results': senate_2014_results
        }
        
        # Calculate 2014 statewide totals
        total_2014_dem = sum(r['dem_votes'] for r in senate_2014_results.values())
        total_2014_rep = sum(r['rep_votes'] for r in senate_2014_results.values())
        print(f"2014 statewide totals: Gordon Ball (D) {total_2014_dem:,}, Lamar Alexander (R) {total_2014_rep:,}")
        
    except FileNotFoundError:
        print("\n2014 CSV file not found, skipping 2014 update")
    except Exception as e:
        print(f"\nError loading 2014 data: {e}")
    
    # Save the updated JSON
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nUpdated county results saved to all_county_results.json")
    print("Counties updated:")
    for county in sorted(senate_2006_results.keys())[:10]:  # Show first 10
        r = senate_2006_results[county]
        print(f"  {county}: {r['competitiveness']['description']}")

if __name__ == "__main__":
    main()