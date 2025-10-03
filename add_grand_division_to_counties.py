import geopandas as gpd

# Mapping from county name to grand division (based on official TN PDF)
GRAND_DIVISION_MAP = {
    # East Tennessee
    'Anderson': 'East', 'Bedford': 'Middle', 'Benton': 'West', 'Bledsoe': 'East', 'Blount': 'East', 'Bradley': 'East', 'Campbell': 'East', 'Cannon': 'Middle', 'Carroll': 'West', 'Carter': 'East',
    'Cheatham': 'Middle', 'Chester': 'West', 'Claiborne': 'East', 'Clay': 'Middle', 'Cocke': 'East', 'Coffee': 'Middle', 'Crockett': 'West', 'Cumberland': 'East', 'Davidson': 'Middle', 'Decatur': 'West',
    'DeKalb': 'Middle', 'Dickson': 'Middle', 'Dyer': 'West', 'Fayette': 'West', 'Fentress': 'East', 'Franklin': 'Middle', 'Gibson': 'West', 'Giles': 'Middle', 'Grainger': 'East', 'Greene': 'East',
    'Grundy': 'Middle', 'Hamblen': 'East', 'Hamilton': 'East', 'Hancock': 'East', 'Hardeman': 'West', 'Hardin': 'West', 'Hawkins': 'East', 'Haywood': 'West', 'Henderson': 'West', 'Henry': 'West',
    'Hickman': 'Middle', 'Houston': 'Middle', 'Humphreys': 'Middle', 'Jackson': 'Middle', 'Jefferson': 'East', 'Johnson': 'East', 'Knox': 'East', 'Lake': 'West', 'Lauderdale': 'West', 'Lawrence': 'Middle',
    'Lewis': 'Middle', 'Lincoln': 'Middle', 'Loudon': 'East', 'McMinn': 'East', 'McNairy': 'West', 'Macon': 'Middle', 'Madison': 'West', 'Marion': 'East', 'Marshall': 'Middle', 'Maury': 'Middle',
    'Meigs': 'East', 'Monroe': 'East', 'Montgomery': 'Middle', 'Moore': 'Middle', 'Morgan': 'East', 'Obion': 'West', 'Overton': 'Middle', 'Perry': 'Middle', 'Pickett': 'East', 'Polk': 'East',
    'Putnam': 'Middle', 'Rhea': 'East', 'Roane': 'East', 'Robertson': 'Middle', 'Rutherford': 'Middle', 'Scott': 'East', 'Sequatchie': 'East', 'Sevier': 'East', 'Shelby': 'West', 'Smith': 'Middle',
    'Stewart': 'Middle', 'Sullivan': 'East', 'Sumner': 'Middle', 'Tipton': 'West', 'Trousdale': 'Middle', 'Unicoi': 'East', 'Union': 'East', 'Van Buren': 'Middle', 'Warren': 'Middle', 'Washington': 'East',
    'Wayne': 'Middle', 'Weakley': 'West', 'White': 'Middle', 'Williamson': 'Middle', 'Wilson': 'Middle'
}

COUNTY_GEOJSON = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\VTDs\TN_counties.geojson"
OUTPUT = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\VTDs\TN_counties_with_grand.geojson"

gdf = gpd.read_file(COUNTY_GEOJSON)
gdf['Grand'] = gdf['NAME'].map(GRAND_DIVISION_MAP)
gdf.to_file(OUTPUT, driver='GeoJSON')
print(f"Added Grand Division to counties and saved to {OUTPUT}")
