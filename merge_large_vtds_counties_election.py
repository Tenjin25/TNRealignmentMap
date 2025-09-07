import json
import os
import pandas as pd
from shapely.geometry import shape
from shapely.prepared import prep
from tqdm import tqdm

# Paths
base = os.path.dirname(__file__)
vtds_path = os.path.join(base, 'VTDs', 'tn_vtds_2000s_merged.geojson')
counties_path = os.path.join(base, 'VTDs', 'TN_counties_with_grand.geojson')
election_path = os.path.join(base, 'merged_election_data.csv')
out_path = os.path.join(base, 'vtds_counties_election_merged.geojson')

# Load counties (small, so in memory)
with open(counties_path, 'r', encoding='utf-8') as f:
    counties_gj = json.load(f)
counties = [
    {
        'geometry': shape(feat['geometry']),
        'props': feat['properties']
    }
    for feat in counties_gj['features']
]
for c in counties:
    c['prepared'] = prep(c['geometry'])

# Load election data (in memory)
election = pd.read_csv(election_path, dtype=str, low_memory=False)

# Helper: find county for a VTD feature
def find_county(vtd_geom):
    for c in counties:
        if c['prepared'].intersects(vtd_geom):
            return c['props']
    return {}

# Helper: find election row for a VTD feature
def find_election_row(vtd_props):
    # Try to match on precinct and county name
    for p_col in ['PRECINCT', 'Precinct', 'precinct', 'VTD', 'VTDNAME']:
        for c_col in ['COUNTYNAME', 'County', 'county']:
            if p_col in vtd_props and c_col in vtd_props:
                matches = election[(election[p_col] == vtd_props[p_col]) & (election[c_col] == vtd_props[c_col])]
                if not matches.empty:
                    return matches.iloc[0].to_dict()
    return {}

# Stream VTDs, merge, and write output
with open(vtds_path, 'r', encoding='utf-8') as f_in, open(out_path, 'w', encoding='utf-8') as f_out:
    # Write header
    f_out.write('{"type": "FeatureCollection", "features": [\n')
    first = True
    for line in f_in:
        if '"type": "Feature"' not in line:
            continue
        feat = json.loads(line.rstrip(',\n'))
        vtd_geom = shape(feat['geometry'])
        vtd_props = feat['properties']
        # Find county
        county_props = find_county(vtd_geom)
        vtd_props.update(county_props)
        # Find election row
        elec_props = find_election_row(vtd_props)
        vtd_props.update(elec_props)
        # Write feature
        if not first:
            f_out.write(',\n')
        json.dump({"type": "Feature", "geometry": feat['geometry'], "properties": vtd_props}, f_out)
        first = False
    f_out.write('\n]}')
print(f'Merged file written to {out_path}')
