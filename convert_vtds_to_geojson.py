import geopandas as gpd
import os
import glob

# Directory containing VTD shapefiles for 2010, 2012, 2020, etc.
VTD_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\VTDs\tl_2020_47_vtd20"
OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find all VTD shapefiles (skip 2008 if you already have it)
shapefiles = glob.glob(os.path.join(VTD_DIR, "tl_20*_47_vtd*.shp"))
shapefiles = [s for s in shapefiles if '2008' not in s]

print(f"Found {len(shapefiles)} VTD shapefiles (excluding 2008).")

for shp in shapefiles:
    gdf = gpd.read_file(shp)
    year = ''.join(filter(str.isdigit, os.path.basename(shp)))[:4]
    out_path = os.path.join(OUTPUT_DIR, f"tn_vtds_{year}.geojson")
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"Saved {out_path}")

print("All VTD shapefiles converted to GeoJSON (2008 excluded).")
