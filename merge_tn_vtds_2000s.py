
# NOTE: If you get an ImportError, install geopandas and pandas:
# pip install geopandas pandas
import geopandas as gpd
import pandas as pd
import os
import glob

# Directory where you unzipped all county VTD shapefiles (each county in its own folder)
BASE_DIR = "data/tn_vtds_2000s"  # Change to your actual path
OUTPUT_PATH = "output/tn_vtds_2000s_merged.geojson"

# Find all VTD shapefiles in subdirectories
glob_pattern = os.path.join(BASE_DIR, "**", "tl_2008_*_vtd00.shp")
shapefiles = glob.glob(glob_pattern, recursive=True)

print(f"Found {len(shapefiles)} VTD shapefiles.")

# Read and concatenate all VTDs
gdfs = []
for shp in shapefiles:
    gdf = gpd.read_file(shp)
    gdf["SOURCE_FILE"] = os.path.basename(shp)
    gdfs.append(gdf)

if not gdfs:
    raise RuntimeError("No VTD shapefiles found. Check your BASE_DIR and file structure.")

merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

# Save as a single GeoJSON
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
merged.to_file(OUTPUT_PATH, driver="GeoJSON")
print(f"Merged VTDs saved to {OUTPUT_PATH}")
