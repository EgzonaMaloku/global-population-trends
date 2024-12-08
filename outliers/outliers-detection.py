import pandas as pd
from scipy.stats import zscore
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

file_path = '../data/dataset_04.csv'
data = pd.read_csv(file_path)

base_columns = ["Population", "Median Age", "Yearly Change", "Density (P/Km²)", "Migration_Rate", "Annual_Population_Growth"]

# Step 1: Detect Outliers Using Z-Score
def detect_outliers_zscore(data, columns, threshold):
    z_outliers = {}
    for col in columns:
        if col in data.columns:
            z_scores = zscore(data[col].dropna())
            z_outliers[col] = data[abs(z_scores) > threshold]
    return z_outliers

# Step 2: Detect Outliers Using DBSCAN
def detect_outliers_dbscan(data, columns, eps, min_samples):
    dbscan_outliers = {}
    scaler = StandardScaler()
    for col in columns:
        if col in data.columns:
            col_data = data[col].dropna().values.reshape(-1, 1)
            scaled_data = scaler.fit_transform(col_data)
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(scaled_data)
            dbscan_outliers[col] = data.iloc[data[col].dropna().index[labels == -1]]
    return dbscan_outliers

# Step 3: Experiment with Z-Score and DBSCAN Parameters
def experiment_with_parameters(data, columns):
    best_threshold = None
    best_eps = None
    best_min_samples = None
    min_outliers = float('inf')

    for threshold in [2.5, 3, 3.5]:
        z_outliers = detect_outliers_zscore(data, columns, threshold)
        z_total_outliers = sum([len(outliers) for outliers in z_outliers.values()])
        
        for eps in [0.3, 0.5, 0.7]:
            for min_samples in [3, 5, 10]:
                dbscan_outliers = detect_outliers_dbscan(data, columns, eps, min_samples)
                dbscan_total_outliers = sum([len(outliers) for outliers in dbscan_outliers.values()])
                total_outliers = z_total_outliers + dbscan_total_outliers
                
                if total_outliers < min_outliers:
                    min_outliers = total_outliers
                    best_threshold = threshold
                    best_eps = eps
                    best_min_samples = min_samples

    print(f"Best Z-Score Threshold: {best_threshold}")
    print(f"Best DBSCAN eps: {best_eps}")
    print(f"Best DBSCAN min_samples: {best_min_samples}")
    return best_threshold, best_eps, best_min_samples

def handle_outliers_with_zscore_and_dbscan(data, columns, threshold, eps, min_samples):
    z_outliers = detect_outliers_zscore(data, columns, threshold)
    dbscan_outliers = detect_outliers_dbscan(data, columns, eps, min_samples)

    z_indices = set(pd.concat(z_outliers.values()).index)
    dbscan_indices = set(pd.concat(dbscan_outliers.values()).index)
    all_outlier_indices = z_indices.union(dbscan_indices)

    data['is_outlier'] = data.index.isin(all_outlier_indices)

    rows_to_remove = data.index.isin(z_indices)
    rows_removed = rows_to_remove.sum()

    flagged_rows = data[data['is_outlier']].copy()
    flagged_rows.to_csv('flagged_rows.csv', index=False)

    data_after_removal = data[~rows_to_remove].copy()
    data_after_removal = data_after_removal.drop(columns=['is_outlier'])

    rows_flagged = data['is_outlier'].sum()
    print(f"Rows removed: {rows_removed}")
    print(f"Rows flagged as outliers: {rows_flagged}")
    print(f"Rows remaining: {len(data_after_removal)}")

    return data_after_removal


# Step 5: Compare Distributions
def compare_distributions(original_data, adjusted_data, columns):
    for col in columns:
        if col in original_data.columns and col in adjusted_data.columns:
            plt.figure(figsize=(10, 5))
            sns.kdeplot(original_data[col], label="Original", color='red', fill=True, alpha=0.4)
            sns.kdeplot(adjusted_data[col], label="Adjusted", color='blue', fill=True, alpha=0.4)
            plt.title(f"Comparison of {col} Distributions (Original vs Adjusted)")
            plt.xlabel(col)
            plt.ylabel("Density")
            plt.legend()
            plt.show()


if __name__ == "__main__":

    # print("Experimenting with Z-Score and DBSCAN parameters...")
    # best_threshold, best_eps, best_min_samples = experiment_with_parameters(data, base_columns)
    # Best Z-Score Threshold: 3.5
    # Best DBSCAN min_samples: 3
    # Best DBSCAN eps: 0.7

    adjusted_data = handle_outliers_with_zscore_and_dbscan(data.copy(), base_columns, 3.5, 0.7, 3)

    adjusted_data_path = '../data/dataset_05.csv'
    adjusted_data.to_csv(adjusted_data_path, index=False)

    compare_distributions(data, adjusted_data, base_columns)
    print(f"Adjusted dataset (base columns) saved to: {adjusted_data_path}")
