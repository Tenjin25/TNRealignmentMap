import os
import pandas as pd
import geopandas as gpd

# --- Margin category assignment ---

# --- Competitiveness system (from NC) ---
COMPETITIVENESS_CATEGORIES = [
    # Republican
    {"category": "Annihilation", "range": (40, float('inf')), "party": "Republican", "code": "R_ANNIHILATION", "color": "#67000d"},
    {"category": "Dominant", "range": (30, 40), "party": "Republican", "code": "R_DOMINANT", "color": "#a50f15"},
    {"category": "Stronghold", "range": (20, 30), "party": "Republican", "code": "R_STRONGHOLD", "color": "#cb181d"},
    {"category": "Safe", "range": (10, 20), "party": "Republican", "code": "R_SAFE", "color": "#ef3b2c"},
    {"category": "Likely", "range": (5.5, 10), "party": "Republican", "code": "R_LIKELY", "color": "#fb6a4a"},
    {"category": "Lean", "range": (1, 5.5), "party": "Republican", "code": "R_LEAN", "color": "#fcae91"},
    {"category": "Tilt", "range": (0.5, 1), "party": "Republican", "code": "R_TILT", "color": "#fee8c8"},
    # Tossup
    {"category": "Tossup", "range": (-0.5, 0.5), "party": "Tossup", "code": "TOSSUP", "color": "#f7f7f7"},
    # Democratic
    {"category": "Tilt", "range": (-1, -0.5), "party": "Democratic", "code": "D_TILT", "color": "#e1f5fe"},
    {"category": "Lean", "range": (-5.5, -1), "party": "Democratic", "code": "D_LEAN", "color": "#c6dbef"},
    {"category": "Likely", "range": (-10, -5.5), "party": "Democratic", "code": "D_LIKELY", "color": "#9ecae1"},
    {"category": "Safe", "range": (-20, -10), "party": "Democratic", "code": "D_SAFE", "color": "#6baed6"},
    {"category": "Stronghold", "range": (-30, -20), "party": "Democratic", "code": "D_STRONGHOLD", "color": "#3182bd"},
    {"category": "Dominant", "range": (-40, -30), "party": "Democratic", "code": "D_DOMINANT", "color": "#08519c"},
    {"category": "Annihilation", "range": (float('-inf'), -40), "party": "Democratic", "code": "D_ANNIHILATION", "color": "#08306b"},
]

def assign_competitiveness(margin_pct):
    for cat in COMPETITIVENESS_CATEGORIES:
        low, high = cat["range"]
        if low < margin_pct <= high:
            return cat
    # Fallback
    return {"category": "Unknown", "party": "Unknown", "code": "UNKNOWN", "color": "#000000"}

# --- Election data extraction ---
def extract_dem_rep_votes(row):
    dem_votes = 0
    rep_votes = 0
    # Pattern 1: 2008-2012 (BNAME/TALLY, party in name)
    bname_cols = [col for col in row.index if col.upper().startswith('BNAME')]
    tally_cols = [col for col in row.index if col.upper().startswith('TALLY')]
    if bname_cols and tally_cols:
        for bcol, tcol in zip(bname_cols, tally_cols):
            bname = str(row.get(bcol, '')).upper()
            tally = row.get(tcol, '')
            try:
                tally = int(tally)
            except:
                tally = 0
            if '(D' in bname or '- D' in bname:
                dem_votes += tally
            elif '(R' in bname or '- R' in bname:
                rep_votes += tally
        return dem_votes, rep_votes
    # Pattern 2: 2014+ (RNAME/PARTY/PVTALLY)
    party_cols = [col for col in row.index if col.upper().startswith('PARTY')]
    party_cols = [col for col in row.index if col.upper().startswith('PARTY')]
    pvtally_cols = [col for col in row.index if col.upper().startswith('PVTALLY')]
    if party_cols and pvtally_cols:
        for pcol, tcol in zip(party_cols, pvtally_cols):
            party = str(row.get(pcol, '')).strip().upper()
            tally = row.get(tcol, '')
            try:
                tally = int(tally)
            except:
                tally = 0
            if party.startswith('DEM'):
                dem_votes += tally
            elif party.startswith('REP'):
                rep_votes += tally
        return dem_votes, rep_votes
    # Fallback: 0,0
    return dem_votes, rep_votes

# --- CONFIGURATION ---
# Map each election year to the VTD and county shapefile sources
YEAR_CONFIG = {
    2000: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2000s_merged.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2000_with_county.geojson',
    },
    2008: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2000s_merged.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2008_with_county.geojson',
    },
    2010: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2010.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2010_with_county.geojson',
    },
    2012: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2010.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2012_with_county.geojson',
    },
    2014: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2010.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2014_with_county.geojson',
    },
    2016: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2010.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2016_with_county.geojson',
    },
    2018: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2010.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2018_with_county.geojson',
    },
    2020: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2020.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2020_with_county.geojson',
    },
    2022: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2020.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2022_with_county.geojson',
    },
    2024: {
        'vtd_dir': r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\vtd_geojsons\tn_vtds_2020.geojson',
        'county_shp': 'VTDs/TN_counties.geojson',
        'output': 'output/vtds_with_county/tn_vtds_2024_with_county.geojson',
    },
}


def merge_vtds_with_counties(year):
    config = YEAR_CONFIG[year]
    vtd_path = config['vtd_dir']
    county_shp = config['county_shp']
    output_path = config['output']

    # 1. Load VTDs (GeoJSON)
    vtds = gpd.read_file(vtd_path)

    # 2. Load county shapefile
    counties = gpd.read_file(county_shp)
    counties = counties.to_crs(vtds.crs)

    # 3. Spatial join: assign county info to each VTD
    vtds_with_county = gpd.sjoin(vtds, counties, how='left', predicate='intersects')

    print("Columns in vtds_with_county after spatial join:")
    print(vtds_with_county.columns.tolist())
    # 4. Merge with election data
    election_csv = f"Election_Data/standardized/{year}_standardized.csv"
    if os.path.exists(election_csv):
        df_elec = pd.read_csv(election_csv, dtype=str)
        # Strip whitespace from all column names
        df_elec.columns = df_elec.columns.str.strip()
        # Clean whitespace in key columns
        df_elec['COUNTY'] = df_elec['COUNTY'].astype(str).str.strip()
        df_elec['PRECINCT'] = df_elec['PRECINCT'].astype(str).str.strip()

        # For 2008, 2010, 2012: map FIPS to county names
        if year in [2008, 2010, 2012]:
            fips_path = 'tn_county_fips.csv'
            fips_df = pd.read_csv(fips_path, dtype=str)
            fips_df['FIPS'] = fips_df['FIPS'].str.zfill(3)
            fips_df['COUNTY'] = fips_df['COUNTY'].str.strip().str.upper()
            # Remove leading zeros from election data county codes, then zfill(3)
            df_elec['COUNTY_FIPS'] = df_elec['COUNTY'].str.lstrip('0').str.zfill(3)
            df_elec = df_elec.merge(fips_df, left_on='COUNTY_FIPS', right_on='FIPS', how='left', suffixes=('', '_FIPS'))
            # Use county name from FIPS mapping
            fips_map = dict(zip(fips_df['FIPS'], fips_df['COUNTY']))
            # After merge, there may be duplicate COUNTY_FIPS columns; select the left-side one for mapping
            # Robustly select the correct Series for mapping (avoid DataFrame)
            if 'COUNTY_FIPS_x' in df_elec.columns:
                county_fips_series = df_elec['COUNTY_FIPS_x']
            elif 'COUNTY_FIPS' in df_elec.columns:
                county_fips_series = df_elec['COUNTY_FIPS']
            else:
                raise Exception('COUNTY_FIPS column not found after merge')
            # If for any reason this is a DataFrame, select the first column
            if hasattr(county_fips_series, 'ndim') and getattr(county_fips_series, 'ndim', 1) > 1:
                county_fips_series = county_fips_series.iloc[:, 0]
            county_fips_series = county_fips_series.astype(str)
            # Map FIPS to county name
            df_elec['COUNTY'] = county_fips_series.map(fips_map)
            # If mapping fails (NaN), fallback to original COUNTY_FIPS value
            df_elec['COUNTY'] = df_elec['COUNTY'].fillna(county_fips_series)
            df_elec['COUNTY'] = df_elec['COUNTY'].astype(str).str.strip().str.upper()
        
        # Calculate margin and category for each row
        dem_votes, rep_votes, margin, margin_pct, winner, comp_cat, comp_party, comp_code, comp_color = [], [], [], [], [], [], [], [], []
        if os.path.exists(election_csv):
            df_elec = pd.read_csv(election_csv, dtype=str)
            # Strip whitespace from all column names
            df_elec.columns = df_elec.columns.str.strip()
            # Clean whitespace in key columns
            df_elec['COUNTY'] = df_elec['COUNTY'].astype(str).str.strip()
            df_elec['PRECINCT'] = df_elec['PRECINCT'].astype(str).str.strip()

            # For 2008, 2010, 2012: map FIPS to county names
            if year in [2008, 2010, 2012]:
                fips_path = 'tn_county_fips.csv'
                fips_df = pd.read_csv(fips_path, dtype=str)
                fips_df['FIPS'] = fips_df['FIPS'].str.zfill(3)
                fips_df['COUNTY'] = fips_df['COUNTY'].str.strip().str.upper()
                # Remove leading zeros from election data county codes, then zfill(3)
                df_elec['COUNTY_FIPS'] = df_elec['COUNTY'].str.lstrip('0').str.zfill(3)
                df_elec = df_elec.merge(fips_df, left_on='COUNTY_FIPS', right_on='FIPS', how='left', suffixes=('', '_FIPS'))
                # Use county name from FIPS mapping
                fips_map = dict(zip(fips_df['FIPS'], fips_df['COUNTY']))
                # After merge, there may be duplicate COUNTY_FIPS columns; select the left-side one for mapping
                # Robustly select the correct Series for mapping (avoid DataFrame)
                if 'COUNTY_FIPS_x' in df_elec.columns:
                    county_fips_series = df_elec['COUNTY_FIPS_x']
                elif 'COUNTY_FIPS' in df_elec.columns:
                    county_fips_series = df_elec['COUNTY_FIPS']
                else:
                    raise Exception('COUNTY_FIPS column not found after merge')
                # If for any reason this is a DataFrame, select the first column
                if hasattr(county_fips_series, 'ndim') and getattr(county_fips_series, 'ndim', 1) > 1:
                    county_fips_series = county_fips_series.iloc[:, 0]
                county_fips_series = county_fips_series.astype(str)
                # Map FIPS to county name
                df_elec['COUNTY'] = county_fips_series.map(fips_map)
                # If mapping fails (NaN), fallback to original COUNTY_FIPS value
                df_elec['COUNTY'] = df_elec['COUNTY'].fillna(county_fips_series)
                df_elec['COUNTY'] = df_elec['COUNTY'].astype(str).str.strip().str.upper()
        
            # Calculate margin and category for each row
            dem_votes, rep_votes, margin, margin_pct, winner, comp_cat, comp_party, comp_code, comp_color = [], [], [], [], [], [], [], [], []
            for _, row in df_elec.iterrows():
                d, r = extract_dem_rep_votes(row)
                m = d - r
                pct = (m * 100 / max(d + r, 1)) if (d + r) > 0 else 0
                dem_votes.append(d)
                rep_votes.append(r)
                margin.append(m)
                margin_pct.append(pct)
                if d > r:
                    win = "DEM"
                elif r > d:
                    win = "REP"
                else:
                    win = "TOSSUP"
                winner.append(win)
                comp = assign_competitiveness(pct)
                comp_cat.append(comp["category"])
                comp_party.append(comp["party"])
                comp_code.append(comp["code"])
                comp_color.append(comp["color"])
            df_elec['dem_votes'] = dem_votes
            df_elec['rep_votes'] = rep_votes
            df_elec['margin'] = margin
            df_elec['margin_pct'] = margin_pct
            df_elec['winner'] = winner
            df_elec['competitiveness_category'] = comp_cat
            df_elec['competitiveness_party'] = comp_party
            df_elec['competitiveness_code'] = comp_code
            df_elec['competitiveness_color'] = comp_color
            # Merge with spatial by county+precinct (adjust as needed)
            vtds_with_county['NAME'] = vtds_with_county['NAME'].astype(str).str.strip().str.upper()
            vtds_with_county['PRECINCT'] = vtds_with_county['PRECINCT'].astype(str).str.strip() if 'PRECINCT' in vtds_with_county.columns else ''
            # Print unique join keys for diagnostics (before merging)
            print("Unique spatial NAMEs:", vtds_with_county['NAME'].unique()[:20])
            print("Unique spatial PRECINCTs:", vtds_with_county['PRECINCT'].unique()[:20])
            print("Unique election COUNTYs:", df_elec['COUNTY'].unique()[:20])
            print("Unique election PRECINCTs:", df_elec['PRECINCT'].unique()[:20])
            merged = vtds_with_county.merge(df_elec, left_on=['NAME', 'PRECINCT'], right_on=['COUNTY', 'PRECINCT'], how='left')
        else:
            merged = vtds_with_county
    parser.add_argument('--year', type=int, choices=list(YEAR_CONFIG.keys()), required=True, help='Election year (2000, 2010, 2020)')
    args = parser.parse_args()
    merge_vtds_with_counties(args.year)
