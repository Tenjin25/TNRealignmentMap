import requests
import json

def download_tn_counties():
    """Download Tennessee county boundaries from the US Census Bureau"""
    
    try:
        # Try US Census Cartographic Boundary Files API
        print("Downloading Tennessee counties from US Census...")
        url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_47_county_20m.zip"
        
        # For now, let's try a simpler GeoJSON source
        print("Trying GeoJSON source...")
        geojson_url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson"
        
        response = requests.get(geojson_url)
        response.raise_for_status()
        
        us_counties = response.json()
        print(f"Downloaded {len(us_counties['features'])} total features")
        
        # Filter for Tennessee counties (look for different property names)
        tn_counties = {
            "type": "FeatureCollection",
            "features": []
        }
        
        # Check what properties are available
        if us_counties['features']:
            sample_props = us_counties['features'][0]['properties']
            print("Sample properties:", list(sample_props.keys()))
        
        # Try different property names for state identification
        for feature in us_counties['features']:
            props = feature['properties']
            state_id = props.get('STATE', props.get('STATEFP', props.get('state', '')))
            
            if state_id == '47' or state_id == 47:
                tn_counties['features'].append(feature)
        
        if len(tn_counties['features']) == 0:
            # Try looking for Tennessee by name
            for feature in us_counties['features']:
                props = feature['properties']
                state_name = props.get('STATE_NAME', props.get('state_name', ''))
                if 'tennessee' in state_name.lower() or 'tn' in state_name.lower():
                    tn_counties['features'].append(feature)
        
        print(f"Found {len(tn_counties['features'])} Tennessee counties")
        
        if len(tn_counties['features']) == 0:
            # Create a simple Tennessee county list from your FIPS file
            print("No counties found in GeoJSON, creating simple boundaries...")
            return create_simple_tn_counties()
        
        # Save to file
        with open('tn_counties.geojson', 'w') as f:
            json.dump(tn_counties, f)
        
        print("Saved Tennessee counties to tn_counties.geojson")
        return True
        
    except Exception as e:
        print(f"Error downloading counties: {e}")
        return create_simple_tn_counties()

def create_simple_tn_counties():
    """Create a simple Tennessee counties GeoJSON using your FIPS data"""
    try:
        # Read your FIPS file
        import pandas as pd
        fips_df = pd.read_csv('tn_county_fips.csv')
        
        # Create simple point-based counties for now
        tn_counties = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for _, row in fips_df.iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "NAME": row['County'].replace(' County', ''),
                    "GEOID": f"47{row['FIPS']:03d}",
                    "STATEFP": "47",
                    "COUNTYFP": f"{row['FIPS']:03d}"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [-86.5, 35.5]  # Tennessee center point
                }
            }
            tn_counties['features'].append(feature)
        
        with open('tn_counties.geojson', 'w') as f:
            json.dump(tn_counties, f)
        
        print(f"Created simple Tennessee counties with {len(tn_counties['features'])} counties")
        return True
        
    except Exception as e:
        print(f"Error creating simple counties: {e}")
        return False

if __name__ == "__main__":
    download_tn_counties()