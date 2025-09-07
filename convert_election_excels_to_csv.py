import pandas as pd
import os

# List of election data files to convert
files = [
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\November2010.xls",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\November2008.xlsx",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\20141104_PrecinctTotals.xlsx",
    r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\Election_Data\November2012.xlsx"
]

OUTPUT_DIR = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\TNRealignments\output\election_csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in files:
    print(f"Processing {file}")
    # Read Excel file (auto-detects .xls or .xlsx)
    df = pd.read_excel(file)
    # Save as CSV
    csv_name = os.path.splitext(os.path.basename(file))[0] + ".csv"
    out_path = os.path.join(OUTPUT_DIR, csv_name)
    df.to_csv(out_path, index=False)
    print(f"Saved {out_path}")

print("All election files converted to CSV.")
