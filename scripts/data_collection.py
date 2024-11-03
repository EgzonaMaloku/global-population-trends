import pandas as pd

def collect_data():
    """Collect and merge population data from historical and forecasted datasets."""
    population_df = pd.read_csv('../data/original_world-population.csv')
    forecast_df = pd.read_csv('../data/original_world-forecast.csv')

    population_df['DataType'] = 'Historical'
    forecast_df['DataType'] = 'Forecasted'
    
    merged_df = pd.concat([population_df, forecast_df])
    merged_df = merged_df.sort_values(by=["country", "Year"]).reset_index(drop=True)
    merged_df.to_csv('../data/original_merged_dataset.csv', index=False)
    
    print("Data collection completed. File saved as 'original_merged_dataset.csv'.")
    return merged_df



