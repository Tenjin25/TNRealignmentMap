import csv

# Increase CSV field size limit
csv.field_size_limit(1000000)

filename = "Election_Data/standardized/2004_standardized_long.csv"

print("Checking 2004 data...")
with open(filename, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    print(f"Columns: {list(reader.fieldnames)}")
    
    # Check first few rows
    for i, row in enumerate(reader):
        if i < 5:
            print(f"Row {i+1}: {dict(row)}")
        else:
            break