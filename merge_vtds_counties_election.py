import geopandas as gpd
import pandas as pd
import os

# Paths to input files
dir_path = os.path.dirname(__file__)
vtds_path = os.path.join(dir_path, 'VTDs', 'tn_vtds_2000s_merged.geojson')
counties_path = os.path.join(dir_path, 'VTDs', 'TN_counties_with_grand.geojson')
election_path = os.path.join(dir_path, 'merged_election_data.csv')

# Load VTDs and counties
vtds = gpd.read_file(vtds_path)
counties = gpd.read_file(counties_path)

# Load election data
if os.path.exists(election_path):
    election = pd.read_csv(election_path, dtype=str, low_memory=False)
else:
    election = None

# Merge VTDs with counties (spatial join)
vtds_with_county = gpd.sjoin(vtds, counties[['geometry', 'COUNTYFP', 'COUNTYNAME', 'Grand']], how='left', predicate='intersects')

# If election data exists, try to join on precinct/county columns
if election is not None:
    # Try to find common columns for join
    possible_precinct_cols = ['PRECINCT', 'Precinct', 'precinct', 'VTD', 'VTDNAME']
    possible_county_cols = ['COUNTYNAME', 'County', 'county']
    vtd_precinct_col = next((c for c in possible_precinct_cols if c in vtds_with_county.columns), None)
    vtd_county_col = next((c for c in possible_county_cols if c in vtds_with_county.columns), None)
    elec_precinct_col = next((c for c in possible_precinct_cols if c in election.columns), None)
    elec_county_col = next((c for c in possible_county_cols if c in election.columns), None)
    if vtd_precinct_col and vtd_county_col and elec_precinct_col and elec_county_col:
        merged = vtds_with_county.merge(
            election,
            left_on=[vtd_precinct_col, vtd_county_col],
            right_on=[elec_precinct_col, elec_county_col],
            how='left',
            suffixes=('', '_elec')
        )
    else:
        print('Could not find matching columns for election join. Outputting VTDs with county only.')
        merged = vtds_with_county
else:
    merged = vtds_with_county

# Output
out_path = os.path.join(dir_path, 'vtds_counties_election_merged.geojson')
merged.to_file(out_path, driver='GeoJSON')
print(f'Merged file written to {out_path}')
