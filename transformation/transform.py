import pandas as pd
import numpy as np
from transformation_functions import *
df = pd.read_csv("../data/dataset_01.csv")


# 1. Smoothing(remove noise from data): Smooth Yearly Change attribute using moving averages.
df['Yearly Change Smoothed(moving-averages)'] = smoothing_by_moving_averages(df['Yearly  Change'])


# 2. Attribute construction: Construct World Urban Population by summing urban population for each country grouped by Year.
df = add_aggregated_urban_population(df)

# 3. Normalization: Normalize Population and Urban Population attributes using min-max normalization (0 to 1).
df['Population Normalized(min-max)'] = normalize_by_min_max(df['Population'])
df['Urban Population Normalized(min-max)'] = normalize_by_min_max(df['Urban Population'])

# 4. Normalization: Normalize Median Age attribute using Z-score normalization.
df['Median Age Normalized(z-score)'] = normalize_by_z_score(df['Median Age'])


# 5. Normalization: Normalize Density attribute using Decimal Scaling normalization.
df['Density Normalized(decimal-scaling)'] = normalize_by_decimal_scaling(df['Density (P/Km²)'])


# 6. Discretization: Divide Median Age and Yearly Change attributes in bins.
age_bins = [0, 2, 39, 59, 200]
age_labels = ['Baby', 'Young Adults', 'Middle-aged Adults', 'Old Adults']
df['Median Age Binned'] = binning_by_boundaries(df['Median Age'], age_bins, age_labels)

df['Yearly Change Binned'] = binning_by_boundaries(df['Yearly  Change'], 3, ['Low', 'Medium', 'High'])


# Save the transformed dataset
df.to_csv("transformed_dataset.csv", index=False)

print("Data transformations completed and saved to 'transformed_dataset.csv'.")