import geopandas as gpd
import os

# Paths to your files

import glob

VTD_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons"
COUNTY_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\VTDs\TN_counties.geojson"
OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtds_with_county"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load counties once
counties = gpd.read_file(COUNTY_PATH)

# Process all VTD GeoJSONs in the directory
vtd_files = glob.glob(os.path.join(VTD_DIR, '*.geojson'))
print(f"Found {len(vtd_files)} VTD GeoJSONs.")
for vtd_path in vtd_files:
	vtds = gpd.read_file(vtd_path)
	vtds = vtds.to_crs(counties.crs)
	vtds_with_county = gpd.sjoin(vtds, counties[['geometry', 'NAME', 'COUNTYFP', 'GEOID']], how='left', predicate='intersects')
	year = ''.join(filter(str.isdigit, os.path.basename(vtd_path)))[:4]
	out_path = os.path.join(OUTPUT_DIR, f"tn_vtds_{year}_with_county.geojson")
	vtds_with_county.to_file(out_path, driver='GeoJSON')
	print(f"Saved joined VTDs to {out_path}")
