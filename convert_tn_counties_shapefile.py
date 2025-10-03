import geopandas as gpd
import json
import os

def convert_shapefile_to_geojson():
    """Convert Tennessee counties shapefile to GeoJSON format"""
    
    # Path to the shapefile
    shapefile_path = "VTDs/tl_2020_47_county20/tl_2020_47_county20.shp"
    output_path = "VTDs/TN_counties.geojson"
    
    try:
        # Read the shapefile
        print(f"Reading shapefile: {shapefile_path}")
        gdf = gpd.read_file(shapefile_path)
        
        # Display basic info about the data
        print(f"Number of counties: {len(gdf)}")
        print(f"Columns: {list(gdf.columns)}")
        print(f"CRS: {gdf.crs}")
        
        # Display first few rows to see the data structure
        print("\nFirst few counties:")
        print(gdf[['NAME20', 'GEOID20', 'ALAND20', 'AWATER20']].head())
        
        # Convert to WGS84 (EPSG:4326) for web mapping
        if gdf.crs != 'EPSG:4326':
            print("Converting to WGS84...")
            gdf = gdf.to_crs('EPSG:4326')
        
        # Clean up the data - keep only relevant columns
        columns_to_keep = ['NAME20', 'GEOID20', 'ALAND20', 'AWATER20', 'geometry']
        available_columns = [col for col in columns_to_keep if col in gdf.columns]
        gdf_clean = gdf[available_columns].copy()
        
        # Rename columns for consistency
        if 'NAME20' in gdf_clean.columns:
            gdf_clean['county_name'] = gdf_clean['NAME20']
        if 'GEOID20' in gdf_clean.columns:
            gdf_clean['fips'] = gdf_clean['GEOID20']
            
        # Convert to GeoJSON
        print(f"Converting to GeoJSON: {output_path}")
        gdf_clean.to_file(output_path, driver='GeoJSON')
        
        # Verify the output
        with open(output_path, 'r') as f:
            geojson_data = json.load(f)
            
        print(f"\nGeoJSON created successfully!")
        print(f"Features count: {len(geojson_data['features'])}")
        print(f"Feature type: {geojson_data['type']}")
        
        # Show sample feature properties
        if geojson_data['features']:
            sample_feature = geojson_data['features'][0]
            print(f"Sample feature properties: {sample_feature['properties']}")
            
        return True
        
    except Exception as e:
        print(f"Error converting shapefile: {e}")
        return False

if __name__ == "__main__":
    convert_shapefile_to_geojson()