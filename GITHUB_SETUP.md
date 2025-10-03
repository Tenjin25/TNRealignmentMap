# TN Political Realignment Map - GitHub Setup

## Required Data Files
- `VTDs/TN_counties.geojson` (county boundaries)
- `VTDs/tn_precincts.geojson` (precinct boundaries)
- `Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json` (election results)

## Directory Structure
- Place all GeoJSON files in the `VTDs/` folder.
- Place all election result JSONs in `Election_Data/standardized/`.
- Place all scripts in `scripts/`.
- Place all stylesheets in `styles/`.

## Setup Steps
1. Ensure all required data files are present and paths in `index.html` and `scripts/map.js` match the above structure.
2. For large GeoJSON files, use Git LFS:
   ```
   git lfs install
   git lfs track "*.geojson"
   git add .gitattributes
   git add VTDs/*.geojson
   git commit -m "Add large GeoJSONs with LFS"
   git push
   ```
3. To run locally:
   ```
   python -m http.server 8000
   ```
   Then open `http://localhost:8000/index.html` in your browser.

## Notes
- If you update data sources, update the file paths in your HTML and JS files accordingly.
- Document any custom scripts or data processing steps in the README.

## Author
Created by Shamar Davis
