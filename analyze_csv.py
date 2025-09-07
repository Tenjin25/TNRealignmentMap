import pandas as pd

# Load the CSV file
df = pd.read_csv('20241105AllbyPrecinct.csv')

# Show basic info and first few rows
print('DataFrame Info:')
df.info()
print('\nFirst 5 rows:')
print(df.head())
