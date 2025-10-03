import json

data = json.load(open('all_county_results.json'))
senate_2014 = data['results_by_year']['2014']['us_senate']['us_senate_2014_1']
print('2014 Senate contest name:', senate_2014['contest_name'])
sample = list(senate_2014['results'].values())[0]
print('Sample county data:')
print(f'County: {sample["county"]}')
print(f'Dem: {sample["dem_candidate"]} - {sample["dem_votes"]} votes')
print(f'Rep: {sample["rep_candidate"]} - {sample["rep_votes"]} votes')