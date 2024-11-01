import pandas as pd

population_df = pd.read_csv('../data/original_world-population.csv')
forecast_df = pd.read_csv('../data/original_world-forecast.csv') 

# Add a 'DataType' column to differentiate between historical and forecast data
population_df['DataType'] = 'Historical'
forecast_df['DataType'] = 'Forecasted'
merged_df = pd.concat([population_df, forecast_df])
merged_df = merged_df.sort_values(by=["country", "Year"]).reset_index(drop=True)
merged_df.to_csv('../data/original_merged_dataset.csv', index = False)

try:
    merged_df.to_csv('../data/working_dataset.csv', index=False)
    print("File saved as 'working_dataset.csv'")
except PermissionError:
    merged_df.to_csv('../data/working_dataset.csv', index=False)
    print("Permission denied for 'working_dataset.csv'. Saved as 'working_dataset_new.csv' instead.")






