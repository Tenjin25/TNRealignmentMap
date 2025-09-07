import subprocess

years = [2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024]

for year in years:
    print(f"Processing {year}...")
    result = subprocess.run([
        'python', 'merge_vtds_with_county_by_year.py', '--year', str(year)
    ])
    if result.returncode != 0:
        print(f"Year {year} failed with exit code {result.returncode}")
    else:
        print(f"Year {year} completed successfully.")
