from data_collection import collect_data
from data_preprocessing import set_column_data_types, remove_duplicates, fill_missing_values
from data_aggregation import aggregate_data
from data_sampling import sample_data
from correlation_analysis import calculate_correlation
import pandas as pd

# Step 1: Data Collection
data = collect_data()

# Step 2: Data Preprocessing
data = set_column_data_types(data)
data = remove_duplicates(data)
data = fill_missing_values(data)
data.to_csv('../processed/preprocessed_data.csv', index=False)

# Step 3: Aggregation by Region and Year
aggregated_data = aggregate_data(data)
aggregated_data.to_csv('../processed/regional_migration_forecast.csv', index=False)

# Step 4: Sampling
sampled_data = sample_data(data)
sampled_data.to_csv('../processed/sampled_data.csv', index=False)


