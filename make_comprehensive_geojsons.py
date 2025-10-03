import geopandas as gpd
import pandas as pd
import os
import glob

# Paths
VTD_GEOJSON = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\tn_vtds_2000s_merged.geojson"
ELECTION_CSV_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data"
OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\geojson_by_year"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def normalize_precinct(name):
    if pd.isnull(name):
        return ''
    return str(name).strip().upper().replace(' ', '').replace('-', '').replace('_', '')

# Load VTDs
vtds = gpd.read_file(VTD_GEOJSON)
vtds['PRECINCT_NORM'] = vtds['NAME'].apply(normalize_precinct) if 'NAME' in vtds.columns else vtds['VTD'].apply(normalize_precinct)

# Process each election CSV
csv_files = glob.glob(os.path.join(ELECTION_CSV_DIR, '*.csv'))
for csv_path in csv_files:
    year = os.path.basename(csv_path).split('_')[0].replace('November', '').replace('PrecinctTotals', '').replace('byPrecinct', '').replace('Nov', '').replace('StateGeneral', '').replace('2014', '2014').replace('2016', '2016')
    df = pd.read_csv(csv_path)
    # Try to find the precinct column
    for col in df.columns:
        if 'precinct' in col.lower():
            df['PRECINCT_NORM'] = df[col].apply(normalize_precinct)
            break
    else:
        print(f"No precinct column found in {csv_path}, skipping.")
        continue
    # Merge
    merged = vtds.merge(df, on='PRECINCT_NORM', how='left', suffixes=('', '_ELECT'))
    out_path = os.path.join(OUTPUT_DIR, f"tn_vtds_{year}_with_election.geojson")
    merged.to_file(out_path, driver="GeoJSON")
    print(f"Saved {out_path}")

print("All comprehensive GeoJSONs created.")
