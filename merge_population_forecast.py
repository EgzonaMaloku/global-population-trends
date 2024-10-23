import pandas as pd

population_df = pd.read_csv('datasets/world-population.csv')
forecast_df = pd.read_csv('datasets/world-forecast.csv') 

# Add a 'DataType' column to differentiate between historical and forecast data
population_df['DataType'] = 'Historical'
forecast_df['DataType'] = 'Forecasted'

merged_df = pd.concat([population_df, forecast_df])
merged_df = merged_df.sort_values(by=["country", "Year"]).reset_index(drop=True)
merged_df.to_csv('merged_population_forecast.csv', index = False)