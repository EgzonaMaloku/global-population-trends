from helpers import *

dataset_path = '../data/original_merged_dataset.csv'
all_countries_path = 'all_countries.csv'


print('-------------------------------------------------------------------------')

print('Unique countries: ', count_unique_countries(dataset_path))

print('-------------------------------------------------------------------------')

print("Missing countries:")
for country in find_missing_countries(dataset_path, all_countries_path):
    print(country)


print('-------------------------------------------------------------------------')
