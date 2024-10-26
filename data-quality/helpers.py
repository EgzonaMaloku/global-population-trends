import pandas as pd
from fuzzywuzzy import process


def count_unique_countries(file_path):
    df = pd.read_csv(file_path)

    unique_countries = df['country'].nunique()

    return unique_countries


def find_missing_countries(file_dataset, file_all_countries):
    threshold = 85

    df_population = pd.read_csv(file_dataset)
    unique_countries_population = df_population['country'].unique()
    
    df_all_countries = pd.read_csv(file_all_countries)
    all_countries = df_all_countries['title'].unique()
    
    missing_countries = []
    for country in all_countries:
        match, score = process.extractOne(country.lower(), [c.lower() for c in unique_countries_population])
        if score < threshold:  # If similarity score is below the threshold, consider it missing
            missing_countries.append(country)
    
    return list(missing_countries)
