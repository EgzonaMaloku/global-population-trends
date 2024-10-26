import pandas as pd

# Load datasets
population_df = pd.read_csv('datasets/world-population.csv')
forecast_df = pd.read_csv('datasets/world-forecast.csv')

# Add 'DataType' column to distinguish between historical and forecast data
population_df['DataType'] = 'Historical'
forecast_df['DataType'] = 'Forecasted'

# Merge datasets
merged_df = pd.concat([population_df, forecast_df])

# Data type definitions and formatting
merged_df = merged_df.rename(columns=str.strip)  
merged_df['country'] = merged_df['country'].astype(str).str.strip()  # Ensure 'country' is string and trim spaces
merged_df['Year'] = pd.to_numeric(merged_df['Year'], errors='coerce').astype('Int64')  # Convert 'Year' to nullable integer
merged_df['Population'] = pd.to_numeric(merged_df['Population'], errors='coerce').astype('Int64')  # Convert 'Population' to nullable integer
merged_df['DataType'] = merged_df['DataType'].astype('category')  # Using 'category' for 'DataType' to save memory

# Sort and save dataset
merged_df = merged_df.sort_values(by=["country", "Year"]).reset_index(drop=True)
merged_df.to_csv('main_dataset.csv', index=False)

# Check data types
print("Data Types:\n", merged_df.dtypes)

# first few rows for inspection
print("\nSample Data:\n", merged_df.head())

# Missing Values
print("\nMissing Values:\n", merged_df.isnull().sum())

# # Display statistical summary
# print("\nStatistical Summary:\n", merged_df.describe(include='all'))

# # Check unique values for 'DataType' and 'country' (example categorical columns)
# print("\nUnique 'DataType' Values:\n", merged_df['DataType'].unique())
# print("\nUnique 'country' Values:\n", merged_df['country'].unique()[:10])  # Display first 10 unique countries