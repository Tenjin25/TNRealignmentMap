import geopandas as gpd
import os
import glob

# Directory containing all unzipped county VTD shapefiles
BASE_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\data\tn_vtds_2000s"
OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\tn_vtds_2000s_csvs"

# Find all VTD shapefiles in subdirectories
glob_pattern = os.path.join(BASE_DIR, "**", "tl_2008_*_vtd00.shp")
shapefiles = glob.glob(glob_pattern, recursive=True)

print(f"Found {len(shapefiles)} VTD shapefiles.")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for shp in shapefiles:
    gdf = gpd.read_file(shp)
    csv_name = os.path.splitext(os.path.basename(shp))[0] + ".csv"
    out_path = os.path.join(OUTPUT_DIR, csv_name)
    gdf.drop(columns='geometry').to_csv(out_path, index=False)
    print(f"Saved {out_path}")

print("All shapefiles converted to CSV.")
