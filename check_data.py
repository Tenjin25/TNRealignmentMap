import json

data = json.load(open('all_county_results.json'))
years = sorted(data['results_by_year'].keys())
print('Available years:', years)
print()

print('US Senate contests:')
for year in years:
    contests = data['results_by_year'][year]
    if 'us_senate' in contests:
        senate_contests = list(contests['us_senate'].keys())
        print(f'  {year}: {senate_contests}')
        # Check if 2006 data looks correct
        if year == '2006':
            contest = contests['us_senate']['us_senate_2006_1']
            sample_county = list(contest['results'].values())[0]
            print(f'    Sample county: {sample_county["county"]}')
            print(f'    Dem candidate: {sample_county["dem_candidate"]}')
            print(f'    Rep candidate: {sample_county["rep_candidate"]}')
            print(f'    Dem votes: {sample_county["dem_votes"]}')

print()
print('All contest types by year:')
for year in years:
    contests = data['results_by_year'][year]
    print(f'{year}: {list(contests.keys())}')