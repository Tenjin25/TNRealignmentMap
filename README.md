# Tennessee VTDs and Election Data Project

This repository contains scripts and data for working with Tennessee Voting Tabulation Districts (VTDs), county boundaries, and precinct-level election results from 2008–2024.

## Features
- Download and merge VTD shapefiles from the Census and TDOT
- Convert shapefiles to GeoJSON for web mapping
- Join VTDs with county boundaries
- Convert and clean election data from Excel/CSV
- Create comprehensive GeoJSONs for mapping and analysis
- Scripts for simplifying GeoJSONs for web use
- Git LFS support for large files

## Directory Structure
- `VTDs/` — Raw and processed VTD and county shapefiles/GeoJSONs
- `output/` — Merged, joined, and simplified GeoJSONs
- `Election_Data/` — Raw and processed election results
- `scripts/` — Python scripts for all processing steps

## Usage
1. **Install requirements:**
   ```
   pip install geopandas pandas requests
   ```
2. **Download and process VTDs:**
   - Use `download_tn_vtds_2000s.py` to fetch 2000s VTDs
   - Use `convert_vtds_to_geojson.py` and `convert_counties_to_geojson.py` to convert shapefiles to GeoJSON
3. **Join VTDs with counties:**
   - Run `join_vtds_with_counties.py` to add county info to each VTD
4. **Convert and join election data:**
   - Use `convert_election_excels_to_csv.py` to convert Excel to CSV
   - Use `make_comprehensive_geojsons.py` to join election results to VTDs
5. **Simplify for web mapping:**
   - Use the provided simplification script to reduce GeoJSON size for Mapbox GL JS
6. **Version large files with Git LFS:**
   ```
   git lfs install
   git lfs track "*.geojson"
   git add .gitattributes
   git add output/*.geojson
   git commit -m "Add large GeoJSONs with LFS"
   git push
   ```

## Notes
- Adjust script paths as needed for your environment.
- For best web performance, use simplified GeoJSONs.
- See each script for more details and options.

## Interactive Map (HTML)

The project includes an interactive HTML map (e.g., `ultimate_tn_political_map_CLEAN.html`) for visualizing Tennessee VTDs, counties, and election results using Mapbox GL JS.

### Features
- Toggle between county, grand division, and precinct (VTD) views
- Visualize political categories, swings, and research findings
- Sidebar for county, grand division, and statewide summaries
- Legend and controls for map layers

### How to Use
1. Open the HTML file in your browser (or serve it locally for full functionality).
2. Place your processed/simplified GeoJSONs in the appropriate location and update the data source paths in the HTML/JS as needed.
3. The map will display the VTD and county boundaries, and you can overlay election results by year.

**Note:** For best performance, use simplified GeoJSONs. Large files may cause slow loading or browser issues.

### Customization
- Update the HTML/JS to point to your own GeoJSONs and election data.
- Adjust the map center, zoom, and style as needed for your project.
- To calculate election margins by grand division (East, Middle, West Tennessee), county, and statewide:
   - Ensure your county GeoJSON includes a `Grand` or `GrandDivision` property for each county.
   - In your analysis scripts, group and aggregate election results by this property for grand division margins, by `NAME` for county margins, and sum all for statewide margins.
   - Update the HTML/JS to display these summaries in the sidebar and map overlays.

---
# TN Realignments Project Workspace

## Directory Structure

- `merge_vtds_with_county_by_year.py` — Main script for merging VTDs, counties, and election data by year
- `batch_merge_vtds_with_county.py` — Batch processing for all years
- `Election_Data/standardized/` — Standardized election CSVs (2008–2024)
- `output/` — Output directory for GeoJSONs and comprehensive JSONs
  - `vtds_with_county/` — Merged VTDs-with-county GeoJSONs by year
  - `comprehensive_YYYY.json` — Metadata-rich JSONs for each year
- `VTDs/TN_counties.geojson` — County boundaries
- `tn_county_fips.csv` — County FIPS crosswalk
- `scan_county_precincts.py`, `scan_standardized_csvs.py` — Diagnostics scripts

## Main Workflow

1. **Standardize election data**: Place cleaned CSVs in `Election_Data/standardized/`.
2. **Run merge script**: Use `merge_vtds_with_county_by_year.py --year YYYY` to merge for a specific year.
3. **Batch process**: Use `batch_merge_vtds_with_county.py` to process all years.
4. **Outputs**: Find GeoJSON and JSON outputs in `output/`.

## Diagnostics
- Scripts print join key samples and null diagnostics to help debug merge issues.
- Use scan scripts to inspect unique county/precinct values in source files.

---

*Last updated: September 7, 2025*

## License
MIT
