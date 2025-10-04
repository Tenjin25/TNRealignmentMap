## TN Political Realignment Map (Clean Version)

### Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/TNRealignments.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TNRealignments
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Overview of Categories
This project organizes data into several categories to facilitate analysis and visualization. Here's what each category means:

- **Contests**: Represents different political races or elections, such as gubernatorial, presidential, or senate races.
- **Counties**: Refers to the geographical divisions within Tennessee, each with its own set of election results.
- **VTDs (Voting Tabulation Districts)**: Smaller subdivisions within counties used for reporting election results.
- **Grand Divisions**: Historical and geographical divisions of Tennessee (East, Middle, and West).
- **Election Data**: Includes results for various contests, broken down by county and VTD.
- **GeoJSON Files**: Used for mapping and spatial analysis, representing the geographical boundaries of counties and VTDs.

Understanding these categories will help you navigate the data and use the tools provided in this project effectively.

### Political Categories Explained

The map uses color-coded categories to represent the competitiveness and margin of victory in each county or precinct. These categories are:

- **Annihilation (40%+ margin):** One party wins by more than 40 percentage points. Indicates a landslide victory and a safe stronghold for the winning party.
- **Dominant (30-40% margin):** One party wins by 30-40 percentage points. Still a very safe seat, but slightly less extreme than Annihilation.
- **Stronghold (20-30% margin):** One party wins by 20-30 percentage points. A reliably safe county or precinct for the winning party.
- **Safe (10-20% margin):** One party wins by 10-20 percentage points. The area is considered safe, but not impenetrable.
- **Likely (5.5-10% margin):** The winning party has a clear advantage, but the area could become competitive under the right circumstances.
- **Lean (1-5.5% margin):** The area is competitive, with a modest advantage for the winning party.
- **Tilt (0.5-1% margin):** The area is extremely competitive, with only a slight edge for the winner.
- **Tossup (±0.5% margin):** The margin is less than half a percentage point, indicating a true battleground with no clear favorite.

These categories help users quickly identify which areas are safe for each party, which are competitive, and where political realignment is occurring.

### Contribution Guidelines
We welcome contributions to improve this project! To contribute:
1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure they are well-documented.
3. Test your changes thoroughly.
4. Submit a pull request with a clear description of your changes.

### FAQs
**Q: What Python version is required?**
A: Python 3.7 or higher is recommended.

**Q: How do I report issues or suggest features?**
A: Please use the GitHub Issues tab to report bugs or suggest new features.

**Q: Can I use this project for my own research?**
A: Yes, this project is licensed under the MIT License, so feel free to use it with proper attribution.

This project is an interactive map visualizing Tennessee's county-level and precinct-level political trends from 2004 to 2024.

### Features
- Interactive Mapbox GL JS map of Tennessee
- Sidebar with contest dropdown, county search, and research findings
- County and precinct boundaries (GeoJSON)
- Dynamic county coloring by contest margin
- Statewide results summary for selected contest
- Legend for political categories
- Sidebar toggle (mobile-friendly, accessible)
- Share button (copies map link)
- Accessibility improvements (ARIA, keyboard navigation)
- Responsive design for desktop and mobile

### Usage
1. Open `index.clean.html` in your browser.
2. Select a contest from the dropdown to view results and county coloring.
3. Search for counties using the sidebar search box.
4. Click counties on the map or in the list to zoom and view details.
5. Use the sidebar toggle for mobile or small screens.
6. Click the Share button to copy the map link.

### Data Files
- `Election_Data/spatial/tn_counties.geojson`: County boundaries
- `Election_Data/spatial/tn_precincts.geojson`: Precinct boundaries
- `Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json`: Election results

### Accessibility
- All controls are keyboard accessible.
- ARIA labels and focus management for sidebar and buttons.

### Author
Created by Shamar Davis# Tennessee VTDs and Election Data Project

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

*Last updated: October 3, 2025*

## License
MIT
