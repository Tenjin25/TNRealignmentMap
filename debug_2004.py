import csv

# Increase CSV field size limit
csv.field_size_limit(1000000)

filename = "Election_Data/standardized/2004_standardized.csv"

print("Checking 2004 data...")
with open(filename, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Check all party values
    parties = set()
    rep_count = 0
    total_count = 0
    
    for row in reader:
        total_count += 1
        party = row.get('PARTY', '').strip().upper()
        parties.add(party)
        
        # Check Republican detection
        if party in ["REPUBLICAN", "REP", "R"] or party.startswith("REP"):
            rep_count += 1
            if total_count <= 10:  # Show first few examples
                print(f"Row {total_count}: Party='{party}', Candidate='{row.get('CANDIDATE', '')}', Contest='{row.get('OFFICENAME', '')}'")

print(f"Total rows: {total_count}")
print(f"Unique parties: {sorted(parties)}")
print(f"Republican count: {rep_count}")