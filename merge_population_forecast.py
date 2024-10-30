import pandas as pd

# Load datasets
population_df = pd.read_csv('datasets/world-population.csv')
forecast_df = pd.read_csv('datasets/world-forecast.csv')

# Add 'DataType' column to distinguish between historical and forecast data
population_df['DataType'] = 'Historical'
forecast_df['DataType'] = 'Forecasted'

# Initial check for missing values in 'Migrants (net)'
print("Initial missing values in 'Migrants (net)' column:")
print("Population dataset:", population_df['Migrants (net)'].isnull().sum())
print("Forecast dataset:", forecast_df['Migrants (net)'].isnull().sum())

# Merge datasets
merged_df = pd.concat([population_df, forecast_df])

# Clean and format 'Migrants (net)' column
merged_df['Migrants (net)'] = merged_df['Migrants (net)'].astype(str).str.strip()
merged_df['Migrants (net)'] = merged_df['Migrants (net)'].replace("", pd.NA)
merged_df['Migrants (net)'] = pd.to_numeric(merged_df['Migrants (net)'], errors='coerce')

# Verify missing values after cleanup
print("\nMissing values in 'Migrants (net)' after cleanup:", merged_df['Migrants (net)'].isnull().sum())

# Additional data type definitions and formatting
merged_df = merged_df.rename(columns=str.strip)
merged_df['country'] = merged_df['country'].astype(str).str.strip()
merged_df['Year'] = pd.to_numeric(merged_df['Year'], errors='coerce').astype('Int64')
merged_df['Population'] = pd.to_numeric(merged_df['Population'], errors='coerce').astype('Int64')
merged_df['DataType'] = merged_df['DataType'].astype('category')

# Sort the dataset
merged_df = merged_df.sort_values(by=["country", "Year"]).reset_index(drop=True)

# Attempt saving the dataset, with an alternative name if permission error occurs
try:
    merged_df.to_csv('working_dataset.csv', index=False)
    print("File saved as 'working_dataset.csv'")
except PermissionError:
    merged_df.to_csv('working_dataset_new.csv', index=False)
    print("Permission denied for 'working_dataset.csv'. Saved as 'working_dataset_new.csv' instead.")

# Check data types
print("\nData Types:\n", merged_df.dtypes)

# Sample data for inspection
print("\nSample Data:\n", merged_df.head())

# Missing values summary
print("\nMissing Values:\n", merged_df.isnull().sum())

# Display statistical summary
print("\nStatistical Summary:\n", merged_df.describe(include='all'))

# Check unique values for 'DataType' and 'country'
print("\nUnique 'DataType' Values:\n", merged_df['DataType'].unique())
print("\nUnique 'country' Values:\n", merged_df['country'].unique()[:10])  
