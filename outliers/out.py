import pandas as pd

# File paths for the provided datasets
dataset_path = 'dataset_05.csv'
migration_data_path = 'API_SM.POP.NETM_DS2_en_csv_v2_91.csv'
total_population_data_path = 'API_SP.POP.TOTL_DS2_en_csv_v2_56.csv'

# Load datasets
dataset = pd.read_csv(dataset_path)
migration_data = pd.read_csv(migration_data_path, skiprows=4)  # Skip metadata rows
total_population_data = pd.read_csv(total_population_data_path, skiprows=4)

# Preprocessing the migration dataset
migration_data = migration_data.rename(columns={'Country Name': 'country', 'Indicator Name': 'Indicator'})
migration_data = migration_data.drop(columns=['Country Code', 'Indicator Code'], errors='ignore')

# Preprocessing the total population dataset
total_population_data = total_population_data.rename(columns={'Country Name': 'country', 'Indicator Name': 'Indicator'})
total_population_data = total_population_data.drop(columns=['Country Code', 'Indicator Code'], errors='ignore')

# Reshaping datasets for analysis
migration_data_melted = migration_data.melt(id_vars=['country'], var_name='Year', value_name='Net Migration')
total_population_melted = total_population_data.melt(id_vars=['country'], var_name='Year', value_name='Total Population')

# Clean and convert year columns
migration_data_melted['Year'] = pd.to_numeric(migration_data_melted['Year'], errors='coerce')
total_population_melted['Year'] = pd.to_numeric(total_population_melted['Year'], errors='coerce')

# Aligning migration data with the dataset
aligned_dataset = dataset.merge(
    migration_data_melted, how='left', left_on=['country', 'Year'], right_on=['country', 'Year']
)

# Aligning total population data with the dataset
aligned_dataset = aligned_dataset.merge(
    total_population_melted, how='left', on=['country', 'Year']
)

# Analysis of flagged rows
flagged_rows = aligned_dataset[aligned_dataset['is_outlier'] == True].copy()

# Handle missing data in flagged rows
flagged_rows_cleaned = flagged_rows.dropna(subset=['Net Migration'])

# Check variability before correlation computation
def has_variability(series):
    return len(series.unique()) > 1

# Correlation calculations with checks
if has_variability(flagged_rows_cleaned['Migration_Rate']) and has_variability(flagged_rows_cleaned['Net Migration']):
    correlation_net_migration = flagged_rows_cleaned['Migration_Rate'].corr(flagged_rows_cleaned['Net Migration'])
else:
    correlation_net_migration = None

if has_variability(flagged_rows_cleaned['Density (P/Km²)']) and has_variability(flagged_rows_cleaned['Total Population']):
    correlation_total_population = flagged_rows_cleaned['Density (P/Km²)'].corr(flagged_rows_cleaned['Total Population'])
else:
    correlation_total_population = None

# Determine rows to remove
rows_to_remove = flagged_rows_cleaned[
    (flagged_rows_cleaned['Net Migration'].isna()) |  # Missing migration data
    (flagged_rows_cleaned['Total Population'].isna()) |  # Missing population data
    (flagged_rows_cleaned['Migration_Rate'].abs() > 50)  # Arbitrary condition for extreme values
]

# Save the aligned dataset and rows to remove
aligned_dataset_path = 'aligned_dataset_corrected_final.csv'
rows_to_remove_path = 'rows_to_remove_corrected_final.csv'
aligned_dataset.to_csv(aligned_dataset_path, index=False)
rows_to_remove.to_csv(rows_to_remove_path, index=False)

# Output results
print(f"Aligned dataset saved to: {aligned_dataset_path}")
print(f"Rows to remove saved to: {rows_to_remove_path}")
print(f"Correlation between Migration Rate and Net Migration: {correlation_net_migration}")
print(f"Correlation between Density (P/Km²) and Total Population: {correlation_total_population}")
print(f"Number of flagged rows: {len(flagged_rows)}")
print(f"Number of rows to remove: {len(rows_to_remove)}")  