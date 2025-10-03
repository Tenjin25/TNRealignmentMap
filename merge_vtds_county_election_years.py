import geopandas as gpd
import pandas as pd
import os
import warnings

def merge_vtds_county_election(year):
    base = os.path.dirname(__file__)
    # Load FIPS mapping
    fips_path = os.path.join(base, 'tn_county_fips.csv')
    fips_df = pd.read_csv(fips_path, dtype=str)
    fips_df['COUNTY'] = fips_df['COUNTY'].str.strip().str.upper()
    # Map each election year to the closest available VTDs-with-county file (Census years)
    vtd_year_map = {
        2008: 2000,
        2010: 2010,
        2012: 2010,
        2014: 2010,
        2016: 2010,
        2018: 2010,
        2020: 2020,
        2022: 2020,
        2024: 2020
    }
    vtd_file_year = vtd_year_map.get(year, year)
    vtds_path = os.path.join(base, 'output', 'vtds_with_county', f'tn_vtds_{vtd_file_year}_with_county.geojson')
    # Use standardized election CSV for this year
    election_path = os.path.join(base, 'Election_Data', 'standardized', f'{year}_standardized.csv')
    out_path = os.path.join(base, 'output', f'tn_vtds_{year}_with_county_election.geojson')

    if not os.path.exists(vtds_path):
        print(f"VTDs file for {year} not found: {vtds_path}")
        return
    vtds = gpd.read_file(vtds_path)

    election = pd.read_csv(election_path, dtype=str, low_memory=False)

    # Strip whitespace from COUNTY and PRECINCT columns in both dataframes if present
    for df, col in [(vtds, 'COUNTY'), (vtds, 'PRECINCT'), (election, 'COUNTY'), (election, 'PRECINCT')]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Remove General Assembly races (Tennessee House/Senate)
    office_cols = [c for c in election.columns if 'office' in c.lower() or 'officename' in c.lower()]
    if office_cols:
        office_col = office_cols[0]
        # Exclude rows with 'house' or 'senate' in office name (case-insensitive)
        mask = ~election[office_col].str.lower().str.contains('house|senate', na=False)
        election = election[mask]

    # Explicit join columns for 2020+ (GeoJSON: NAME, NAMELSAD20; CSV: COUNTY, PRECINCT)
    # Strip whitespace from all column names in the election DataFrame
    election.columns = [c.strip() for c in election.columns]
    def find_col(df, candidates):
        cols = {c.strip().upper(): c for c in df.columns}
        for cand in candidates:
            if cand.upper() in cols:
                return cols[cand.upper()]
        return None

    county_col = find_col(election, ['COUNTY'])
    precinct_col = find_col(election, ['PRECINCT'])
    if county_col:
        # Map county names to FIPS
        election.loc[:, county_col] = election[county_col].astype(str).str.strip().str.upper()
        election = election.merge(fips_df, left_on=county_col, right_on='COUNTY', how='left')
    if precinct_col:
        election.loc[:, precinct_col] = election[precinct_col].astype(str).str.strip()
    # Warn if any counties could not be mapped
    if 'FIPS' in election.columns and election['FIPS'].isnull().any():
        warnings.warn('Some counties in the election CSV could not be mapped to FIPS.')
    if year >= 2020:
        # Use 2020+ GeoJSON columns
        for col in ['COUNTYFP', 'NAMELSAD20']:
            if col in vtds.columns:
                vtds[col] = vtds[col].astype(str).str.strip()
        merged = vtds.merge(
            election,
            left_on=['COUNTYFP', 'NAMELSAD20'],
            right_on=['FIPS', precinct_col],
            how='left',
            suffixes=('', '_elec')
        )
        merged.to_file(out_path, driver='GeoJSON')
        print(f"Merged {year} written to {out_path}")
    elif year >= 2012:
        # Use 2012 GeoJSON columns
        for col in ['COUNTYFP', 'NAMELSAD10']:
            if col in vtds.columns:
                vtds[col] = vtds[col].astype(str).str.strip()
        merged = vtds.merge(
            election,
            left_on=['COUNTYFP', 'NAMELSAD10'],
            right_on=['FIPS', precinct_col],
            how='left',
            suffixes=('', '_elec')
        )
        merged.to_file(out_path, driver='GeoJSON')
        print(f"Merged {year} written to {out_path}")
    else:
        print(f"Could not find matching columns for {year}.")

if __name__ == "__main__":
    for year in [2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024]:
        merge_vtds_county_election(year)
