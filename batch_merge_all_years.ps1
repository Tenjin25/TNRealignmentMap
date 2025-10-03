# PowerShell script to batch merge all years into a single JSON
# Adjust the paths as needed for your environment

# Set the base JSON (should be the earliest/empty structure)
$baseJson = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party.json"

# List of year/CSV pairs (edit as needed)
$yearsAndCSVs = @(
    @{year="2004"; csv="Election_Data/standardized/2004_standardized_long.csv"},
    @{year="2006_gov"; csv="Election_Data/standardized/2006_standardized_governor_long.csv"},
    @{year="2006_sen"; csv="Election_Data/standardized/2006_standardized_senate_long.csv"},
    @{year="2008"; csv="Election_Data/standardized/2008_standardized_long.csv"},
    @{year="2010"; csv="Election_Data/standardized/2010_standardized_long.csv"},
    @{year="2012"; csv="Election_Data/standardized/2012_standardized_long.csv"},
    @{year="2014"; csv="Election_Data/standardized/2014_standardized_long.csv"},
    @{year="2016"; csv="Election_Data/standardized/2016_standardized_long.csv"},
    @{year="2018"; csv="Election_Data/standardized/2018_standardized_long.csv"},
    @{year="2020"; csv="Election_Data/standardized/2020_standardized_long.csv"},
    @{year="2022"; csv="Election_Data/standardized/2022_standardized_long.csv"},
    @{year="2024"; csv="Election_Data/standardized/2024_standardized_long.csv"}
)

# Output file
$finalOutput = "Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json"

# Temp file for chaining
$tempInput = $baseJson
$tempOutput = "temp_merge_output.json"

foreach ($item in $yearsAndCSVs) {
    $year = $item.year
    $csv = $item.csv
    Write-Host "Merging $csv for $year..."
    python merge_csv_to_json_flexible.py --json $tempInput --csv $csv --year $year --output $tempOutput --fips tn_county_fips.csv
    # Next input is previous output
    Copy-Item $tempOutput $finalOutput -Force
    $tempInput = $finalOutput
}

# Clean up temp file
Remove-Item $tempOutput -ErrorAction SilentlyContinue

Write-Host "All years merged into $finalOutput"
