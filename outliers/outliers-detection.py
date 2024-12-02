import pandas as pd
from scipy.stats import zscore
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import plotly.express as px
import requests

# Load dataset
file_path = '../data/dataset_04.csv'
data = pd.read_csv(file_path)

# Define column groups
raw_columns = ['Population', 'Urban Population', 'Median Age', 'Yearly  Change', 'Density (P/Km²)']
derived_columns = ['Annual_Population_Growth', 'Migration_Rate', 'Dependency_Ratio', '3_Year_Pop_Avg']
excluded_columns = ['Population Normalized(min-max)', 'Urban Population Normalized(min-max)',
                    'Median Age Normalized(z-score)', 'Density Normalized(decimal-scaling)',
                    'Median Age Binned', 'Yearly Change Binned']

# Step 1: Z-Score Method
def find_outliers_zscore(data, column_name, threshold=3):
    z_scores = zscore(data[column_name].dropna())
    outliers = data[abs(z_scores) > threshold]
    return outliers

# Step 2: Density-Based (DBSCAN) Method
def find_outliers_dbscan(data, column_name, eps=0.5, min_samples=5):
    # Prepare data
    data_scaled = (data[column_name].dropna() - data[column_name].mean()) / data[column_name].std()
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data_scaled.values.reshape(-1, 1))
    outliers = data.iloc[labels == -1]
    return outliers

# Function to detect outliers for selected columns
def detect_outliers_for_columns(data, columns, method, **kwargs):
    outliers_results = {}
    for column in columns:
        if column not in data.columns:
            print(f"Skipping column '{column}': Not found in dataset.")
            continue
        
        if method == 'zscore':
            outliers = find_outliers_zscore(data, column, **kwargs)
        elif method == 'dbscan':
            outliers = find_outliers_dbscan(data, column, **kwargs)
        else:
            raise ValueError("Invalid method. Use 'zscore' or 'dbscan'.")
        
        outliers_results[column] = len(outliers)
    return outliers_results

if __name__ == "__main__":
    print("Detecting outliers in raw and derived columns...\n")

    # Z-Score Outliers for Raw and Derived Columns
    z_outliers_results = detect_outliers_for_columns(data, raw_columns + derived_columns, method='zscore', threshold=3)
    print("Z-Score Outliers Summary:")
    for column, count in z_outliers_results.items():
        print(f"Column: {column}, Outliers: {count}")

    # DBSCAN Outliers for Raw and Derived Columns
    dbscan_outliers_results = detect_outliers_for_columns(data, raw_columns + derived_columns, method='dbscan', eps=0.5, min_samples=5)
    print("\nDBSCAN Outliers Summary:")
    for column, count in dbscan_outliers_results.items():
        print(f"Column: {column}, Outliers: {count}")

    
    columns_to_check = ["Annual_Population_Growth", "Migration_Rate", "Density (P/Km²)"]
    print(f"\nInvestigating columns: {columns_to_check}\n")

    # Extract Z-Score and DBSCAN outliers for the selected columns
    z_outliers_context = {col: find_outliers_zscore(data, col, threshold=3) for col in columns_to_check}
    dbscan_outliers_context = {col: find_outliers_dbscan(data, col, eps=0.5, min_samples=5) for col in columns_to_check}

    # Save Z-Score and DBSCAN outliers to CSV files
    z_outliers_combined = pd.concat([df.assign(Outlier_Type="Z-Score", Column=col) 
                                      for col, df in z_outliers_context.items() if not df.empty])
    dbscan_outliers_combined = pd.concat([df.assign(Outlier_Type="DBSCAN", Column=col) 
                                           for col, df in dbscan_outliers_context.items() if not df.empty])

    z_outliers_file = "z_outliers_selected_columns.csv"
    dbscan_outliers_file = "dbscan_outliers_selected_columns.csv"

    z_outliers_combined.to_csv(z_outliers_file, index=False)
    dbscan_outliers_combined.to_csv(dbscan_outliers_file, index=False)

    print(f"Z-Score Outliers for selected columns saved to '{z_outliers_file}'")
    print(f"DBSCAN Outliers for selected columns saved to '{dbscan_outliers_file}'")
 
 
  # Phase 2 of oulier detection
 
columns_to_check = ["Annual_Population_Growth", "Migration_Rate", "Density (P/Km²)"]

# Extract Z-Score and DBSCAN outliers
z_outliers_combined = pd.concat([find_outliers_zscore(data, col, threshold=3).assign(Outlier_Type="Z-Score", Column=col) for col in columns_to_check])
dbscan_outliers_combined = pd.concat([find_outliers_dbscan(data, col, eps=0.5, min_samples=5).assign(Outlier_Type="DBSCAN", Column=col) for col in columns_to_check])

# Save to CSV
z_outliers_combined.to_csv("z_outliers_selected_columns.csv", index=False)
dbscan_outliers_combined.to_csv("dbscan_outliers_selected_columns.csv", index=False)

# Visualization by Year and Country
for column in columns_to_check:
    z_outliers = z_outliers_combined[z_outliers_combined['Column'] == column]
    dbscan_outliers = dbscan_outliers_combined[dbscan_outliers_combined['Column'] == column]

    # Filter the main dataset to include only rows for outlier countries
    outlier_countries = pd.concat([z_outliers['country'], dbscan_outliers['country']]).unique()
    filtered_data = data[data['country'].isin(outlier_countries)]

    # Interactive Plot using Plotly
    fig = px.scatter(
        data_frame=filtered_data,
        x="Year",
        y=column,
        color="country",
        opacity=0.4,
        title=f'{column} Outliers by Year and Country',
        labels={"Year": "Year", column: column, "country": "Country"},
    )

    if not z_outliers.empty:
        fig.add_scatter(
            x=z_outliers["Year"],
            y=z_outliers[column],
            mode="markers",
            marker=dict(size=10, color="blue"),
            name="Z-Score Outliers",
            text=z_outliers["country"],
        )

    if not dbscan_outliers.empty:
        fig.add_scatter(
            x=dbscan_outliers["Year"],
            y=dbscan_outliers[column],
            mode="markers",
            marker=dict(size=10, color="red"),
            name="DBSCAN Outliers",
            text=dbscan_outliers["country"],
        )

    fig.update_layout(
        showlegend=True,
        xaxis_title="Year",
        yaxis_title=column,
        legend=dict(title="Legend"),
    )
    fig.show()

print("Improved interactive visualizations for Year and Country completed.")