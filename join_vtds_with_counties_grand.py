import geopandas as gpd
import os

def join_vtds_with_counties_grand(year):
    base = os.path.dirname(__file__)
    vtds_path = os.path.join(base, 'output', 'vtd_geojsons', f'tn_vtds_{year}.geojson')
    counties_path = os.path.join(base, 'VTDs', 'TN_counties_with_grand.geojson')
    out_path = os.path.join(base, 'output', 'vtds_with_county', f'tn_vtds_{year}_with_county.geojson')

    if not os.path.exists(vtds_path):
        print(f"VTDs file for {year} not found: {vtds_path}")
        return
    vtds = gpd.read_file(vtds_path)
    counties = gpd.read_file(counties_path)

    # Spatial join
    joined = gpd.sjoin(vtds, counties[['geometry', 'COUNTYFP', 'COUNTYNAME', 'Grand']], how='left', predicate='intersects')
    joined.to_file(out_path, driver='GeoJSON')
    print(f"Joined {year} written to {out_path}")

if __name__ == "__main__":
    for year in [2008, 2010, 2012, 2016, 2018, 2020, 2022, 2024]:
        join_vtds_with_counties_grand(year)
