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
    winner = 'DEM' if dem_votes > rep_votes else 'REP'
    
    # Define competitiveness categories with proper political colors
    if margin < 0.5:
        category = "Tossup"
        base_color = "#2563eb" if winner == 'DEM' else "#dc2626"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_TOSSUP"
    elif margin < 1:
        category = "Tilt"
        base_color = "#bfdbfe" if winner == 'DEM' else "#fca5a5"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_TILT"
    elif margin < 5.5:
        category = "Lean"
        base_color = "#93c5fd" if winner == 'DEM' else "#f87171"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_LEAN"
    elif margin < 10:
        category = "Likely"
        base_color = "#60a5fa" if winner == 'DEM' else "#ef4444"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_LIKELY"
    elif margin < 20:
        category = "Safe"
        base_color = "#3b82f6" if winner == 'DEM' else "#dc2626"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_SAFE"
    elif margin < 30:
        category = "Stronghold"
        base_color = "#1e40af" if winner == 'DEM' else "#991b1b"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_STRONGHOLD"
    elif margin < 40:
        category = "Dominant"
        base_color = "#1e3a8a" if winner == 'DEM' else "#7f1d1d"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_DOMINANT"
    else:
        category = "Annihilation"
        base_color = "#0c1d56" if winner == 'DEM' else "#450a0a"
        party = "Democratic" if winner == 'DEM' else "Republican"
        code = f"{winner}_ANNIHILATION"
    
    description = f"{category} {party}"
    if category == "Tossup":
        description = f"Tossup ({party} Win)"
    
    return {
        'category': category,
        'party': party,
        'code': code,
        'color': base_color,
        'description': description
    }

# Load the PDF-extracted county data
print("Loading 2006 Senate data from PDF extraction...")
df = pd.read_csv('2006_senate_county_totals_from_pdf.csv')

# Filter out rows with zero votes (duplicates from PDF extraction)
df = df[(df['harold_ford_jr'] > 0) | (df['bob_corker'] > 0)]

# Group by county and sum to handle any remaining duplicates
df = df.groupby('county', as_index=False).agg({
    'harold_ford_jr': 'sum',
    'bob_corker': 'sum'
})

print(f"Found {len(df)} counties (Tennessee has 95)")
print(f"Harold Ford Jr. total: {df['harold_ford_jr'].sum():,}")
print(f"Bob Corker total: {df['bob_corker'].sum():,}")

# Load the current JSON
with open('all_county_results.json', 'r') as f:
    data = json.load(f)

# Update 2006 Senate data
if '2006' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2006']:
    contest = data['results_by_year']['2006']['us_senate']['us_senate_2006_1']
    
    # Update contest metadata
    contest['contest_name'] = 'US Senate - Harold Ford Jr. (D) vs Bob Corker (R)'
    contest['dem_candidate'] = 'Harold Ford Jr.'
    contest['rep_candidate'] = 'Bob Corker'
    
    # Process each county
    results = {}
    for _, row in df.iterrows():
        county = row['county'].upper()  # Ensure uppercase to match JSON
        dem_votes = int(row['harold_ford_jr'])
        rep_votes = int(row['bob_corker'])
        other_votes = 0  # We don't have other candidate data from this extraction
        total_votes = dem_votes + rep_votes + other_votes
        two_party_total = dem_votes + rep_votes
        
        if two_party_total > 0:
            dem_pct = (dem_votes / two_party_total) * 100
            rep_pct = (rep_votes / two_party_total) * 100
            margin = abs(dem_votes - rep_votes)
            margin_pct = abs(dem_pct - rep_pct)
            winner = 'DEM' if dem_votes > rep_votes else 'REP'
        else:
            dem_pct = rep_pct = margin = margin_pct = 0
            winner = 'TIE'
        
        comp = calculate_competitiveness(dem_votes, rep_votes)
        
        results[county] = {
            'county': county,
            'contest': 'US Senate',
            'year': '2006',
            'dem_candidate': 'Harold Ford Jr.',
            'rep_candidate': 'Bob Corker',
            'dem_votes': dem_votes,
            'rep_votes': rep_votes,
            'other_votes': other_votes,
            'total_votes': total_votes,
            'two_party_total': two_party_total,
            'margin': margin,
            'margin_pct': margin_pct,
            'winner': winner,
            'competitiveness': comp,
            'all_parties': {
                'DEM': dem_votes,
                'REP': rep_votes,
                'OTHER': other_votes
            },
            'contest_type': 'federal'
        }
    
    contest['results'] = results
    
    # Save updated JSON
    with open('all_county_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nUpdated 2006 Senate data for {len(results)} counties")
    print("\nSample updated counties:")
    for county in list(results.keys())[:5]:
        r = results[county]
        print(f"  {county}: {r['dem_votes']:,} D, {r['rep_votes']:,} R - {r['competitiveness']['description']}")
    
    print("\nUpdated all_county_results.json with complete 2006 Senate data from official PDF")
else:
    print("ERROR: Could not find 2006 US Senate contest in JSON")
