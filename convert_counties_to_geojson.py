import geopandas as gpd
import os
import glob

# Directory containing county shapefiles for 2010, 2020, etc.
COUNTY_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\VTDs"
OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\county_geojsons"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find all county shapefiles
shapefiles = glob.glob(os.path.join(COUNTY_DIR, "tl_20*_47_county*.shp"))

print(f"Found {len(shapefiles)} county shapefiles.")

for shp in shapefiles:
    gdf = gpd.read_file(shp)
    year = ''.join(filter(str.isdigit, os.path.basename(shp)))[:4]
    out_path = os.path.join(OUTPUT_DIR, f"tn_counties_{year}.geojson")
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"Saved {out_path}")

print("All county shapefiles converted to GeoJSON.")
