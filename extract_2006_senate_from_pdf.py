#!/usr/bin/env python3
import pdfplumber
import re
import pandas as pd

# Tennessee county names including multi-word ones
TN_COUNTIES = {
    'ANDERSON', 'BEDFORD', 'BENTON', 'BLEDSOE', 'BLOUNT', 'BRADLEY', 'CAMPBELL', 
    'CANNON', 'CARROLL', 'CARTER', 'CHEATHAM', 'CHESTER', 'CLAIBORNE', 'CLAY', 
    'COCKE', 'COFFEE', 'CROCKETT', 'CUMBERLAND', 'DAVIDSON', 'DECATUR', 'DEKALB', 
    'DICKSON', 'DYER', 'FAYETTE', 'FENTRESS', 'FRANKLIN', 'GIBSON', 'GILES', 
    'GRAINGER', 'GREENE', 'GRUNDY', 'HAMBLEN', 'HAMILTON', 'HANCOCK', 'HARDEMAN', 
    'HARDIN', 'HAWKINS', 'HAYWOOD', 'HENDERSON', 'HENRY', 'HICKMAN', 'HOUSTON', 
    'HUMPHREYS', 'JACKSON', 'JEFFERSON', 'JOHNSON', 'KNOX', 'LAKE', 'LAUDERDALE', 
    'LAWRENCE', 'LEWIS', 'LINCOLN', 'LOUDON', 'MACON', 'MADISON', 'MARION', 
    'MARSHALL', 'MAURY', 'MCMINN', 'MCNAIRY', 'MEIGS', 'MONROE', 'MONTGOMERY', 
    'MOORE', 'MORGAN', 'OBION', 'OVERTON', 'PERRY', 'PICKETT', 'POLK', 'PUTNAM', 
    'RHEA', 'ROANE', 'ROBERTSON', 'RUTHERFORD', 'SCOTT', 'SEQUATCHIE', 'SEVIER', 
    'SHELBY', 'SMITH', 'STEWART', 'SULLIVAN', 'SUMNER', 'TIPTON', 'TROUSDALE', 
    'UNICOI', 'UNION', 'VAN BUREN', 'WARREN', 'WASHINGTON', 'WAYNE', 'WEAKLEY', 
    'WHITE', 'WILLIAMSON', 'WILSON'
}

# Extract data from PDF
pdf = pdfplumber.open('2006_senate_official.pdf')

counties_data = []

for page in pdf.pages:
    text = page.extract_text()
    
    # Split by lines
    lines = text.split('\n')
    
    for line in lines:
        # Look for county data lines (county name followed by numbers)
        # Pattern: COUNTY_NAME followed by numbers separated by spaces
        parts = line.split()
        if len(parts) >= 3:
            # Check if this looks like a data line by finding where numbers start
            try:
                # Find the first numeric part
                num_start_idx = 0
                for i, part in enumerate(parts):
                    try:
                        int(part.replace(',', ''))
                        num_start_idx = i
                        break
                    except ValueError:
                        continue
                
                if num_start_idx >= 1 and num_start_idx < len(parts) - 1:
                    # County name is everything before the first number
                    county_name = ' '.join(parts[:num_start_idx])
                    harold_votes = int(parts[num_start_idx].replace(',', ''))
                    corker_votes = int(parts[num_start_idx + 1].replace(',', ''))
                    
                    # Only include if it's a valid TN county name
                    if county_name in TN_COUNTIES:
                        counties_data.append({
                            'county': county_name,
                            'harold_ford_jr': harold_votes,
                            'bob_corker': corker_votes
                        })
            except (ValueError, IndexError):
                continue

pdf.close()

# Create DataFrame
df = pd.DataFrame(counties_data)

# Calculate totals
harold_total = df['harold_ford_jr'].sum()
corker_total = df['bob_corker'].sum()

print(f"Counties found: {len(df)}")
print(f"\nHarold Ford Jr. total: {harold_total:,}")
print(f"Bob Corker total: {corker_total:,}")
print(f"\nDifference from Wikipedia:")
print(f"Harold Ford Jr.: {879976 - harold_total:,} votes missing")
print(f"Bob Corker: {929911 - corker_total:,} votes missing")

# Show sample
print(f"\nSample counties:")
print(df.head(10))

# Save to CSV
df.to_csv('2006_senate_county_totals_from_pdf.csv', index=False)
print(f"\nSaved to 2006_senate_county_totals_from_pdf.csv")
