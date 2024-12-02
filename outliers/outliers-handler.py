import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
z_outliers_path = 'z_outliers_selected_columns.csv'
dbscan_outliers_path = 'dbscan_outliers_selected_columns.csv'
dataset_path = '../data/dataset_04.csv'

# Load the datasets
z_outliers_combined = pd.read_csv(z_outliers_path).reset_index()
dbscan_outliers_combined = pd.read_csv(dbscan_outliers_path).reset_index()
data = pd.read_csv(dataset_path).reset_index()

# Columns to focus on
columns_to_check = ["Annual_Population_Growth", "Migration_Rate", "Density (P/Km²)"]

# Combine indices of Z-Score and DBSCAN outliers
z_outlier_indices = set(z_outliers_combined['index'])
dbscan_outlier_indices = set(dbscan_outliers_combined['index'])
all_outlier_indices = z_outlier_indices.union(dbscan_outlier_indices)

# Filter rows flagged as outliers
outliers_data = data[data['index'].isin(all_outlier_indices)].copy()

# Step 1: Define Logical Criteria for Handling Outliers
criteria_to_remove = (outliers_data["Migration_Rate"] < -50) | (outliers_data["Density (P/Km²)"] == 0)
criteria_to_impute = (outliers_data["Annual_Population_Growth"] < -0.5) | (outliers_data["Annual_Population_Growth"] > 0.8)
criteria_to_flag = ~(criteria_to_remove | criteria_to_impute)

# Mark rows for removal, imputation, or flagging
outliers_data.loc[:, 'to_remove'] = criteria_to_remove
outliers_data.loc[:, 'to_impute'] = criteria_to_impute
outliers_data.loc[:, 'to_flag'] = criteria_to_flag

# Step 2: Handle Outliers
# Remove rows marked for removal
rows_to_remove = outliers_data[outliers_data['to_remove']]['index']
filtered_data = data[~data['index'].isin(rows_to_remove)].copy()

# Impute rows marked for imputation with the column median
for col in columns_to_check:
    median_value = filtered_data[col].median()
    rows_to_impute = outliers_data[outliers_data['to_impute']]['index']
    filtered_data.loc[filtered_data['index'].isin(rows_to_impute), col] = median_value

# Add a flag for remaining outliers
rows_to_flag = outliers_data[outliers_data['to_flag']]['index']
filtered_data.loc[:, 'is_outlier'] = filtered_data['index'].isin(rows_to_flag)

# Drop the extra index column used for alignment
filtered_data = filtered_data.drop(columns=['index'])

# Save the final dataset
final_dataset_path = 'final_adjusted_dataset.csv'  # Updated path to save locally
filtered_data.to_csv(final_dataset_path, index=False)

# **Added Requirement: Merge final_adjusted_dataset.csv with dataset_04.csv**
# Load final_adjusted_dataset.csv
final_adjusted_data = pd.read_csv(final_dataset_path)

# Ensure both data and final_adjusted_data have 'index' column
if 'index' not in data.columns:
    data = data.reset_index()
if 'index' not in final_adjusted_data.columns:
    final_adjusted_data = final_adjusted_data.reset_index()

# Merge the updated columns back into the original dataset
updated_dataset = data.set_index('index').combine_first(final_adjusted_data.set_index('index')).reset_index()

# Save the merged dataset as dataset_05.csv
updated_dataset_path = '../data/dataset_05.csv'
updated_dataset.to_csv(updated_dataset_path, index=False)

# Step 3: Validate Adjustments
adjusted_stats = filtered_data[columns_to_check].describe()

# Visualize Adjusted Data Distributions
for col in columns_to_check:
    plt.figure(figsize=(10, 5))
    sns.histplot(filtered_data[col], bins=30, kde=True, color='green', label="Adjusted Data")
    plt.title(f"Adjusted Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

rows_removed = len(rows_to_remove)
rows_imputed = len(rows_to_impute)
rows_flagged = filtered_data['is_outlier'].sum()
rows_remaining = filtered_data.shape[0]

print(f"Rows removed based on errors: {rows_removed}")
print(f"Rows imputed based on rare but plausible values: {rows_imputed}")
print(f"Rows flagged as significant anomalies: {rows_flagged}")
print(f"Rows remaining in the dataset: {rows_remaining}")
print(f"Final adjusted dataset saved to: {final_dataset_path}")
print(f"Updated dataset saved to: {updated_dataset_path}")
