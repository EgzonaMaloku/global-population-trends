import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

results_dir = "./results"
os.makedirs(results_dir, exist_ok=True)  

# Multivariate Analysis Description
print("Multivariate Analysis")

# Load the dataset
file_path = "../data/dataset_05.csv" 
df = pd.read_csv(file_path)

# Data Cleaning and Preprocessing
# Remove columns that are not relevant for multivariate analysis
df_clean = df.select_dtypes(include=[np.number]).dropna()  # Only numeric columns, drop missing values

# Calculate Range, Variance
print("Statistical Insights:")
range_df = df_clean.max() - df_clean.min()
variance_df = df_clean.var()
mean_df = df_clean.mean()
std_dev_df = df_clean.std()
median_df = df_clean.median()

stats_df = pd.DataFrame({
    "Range": range_df,
    "Variance": variance_df,
    "Mean": mean_df,
    "Standard Deviation": std_dev_df,
    "Median": median_df,
})


# Save the combined statistics to a CSV file
stats_csv_path = os.path.join(results_dir, "combined_stats.csv")
stats_df.to_csv(stats_csv_path, index_label='Feature')
print(f"Range, variance")

# Correlation Analysis
correlation_matrix = df_clean.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig(os.path.join(results_dir, "correlation_heatmap.png"))
plt.show()

# Pair Plot for Multivariate Analysis --- MULTIVARIATE ANALYSIS
pairplot_path = os.path.join(results_dir, "pairplot.png")
sns.pairplot(df_clean, diag_kind="kde")  # Removed corner=True for full pairplot
plt.savefig(pairplot_path)
print(f"Pair plot saved to {pairplot_path}")
plt.show()

# Principal Component Analysis (PCA)
# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_clean)

# Apply PCA
pca = PCA(n_components=3)  # Select 3 components for visualization
pca_result = pca.fit_transform(scaled_data)

# PCA Variance Explained
print("Explained Variance Ratio by Component:", pca.explained_variance_ratio_)

# PCA Visualization
pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2", "PC3"])
# Check if 'country' column exists in the dataset
if 'country' in df.columns:
    pca_df["Country"] = df["country"].values[:len(pca_df)]  # Add country for context
else:
    pca_df["Country"] = ["Unknown"] * len(pca_df)  # If country column is missing, label as Unknown

plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="Country", palette="tab10")
plt.title("PCA Scatter Plot (First 2 Components)")
plt.savefig(os.path.join(results_dir, "pca_scatter.png"))
plt.show()

# PCA Explained Variance Visualization
plt.figure(figsize=(8, 5))
plt.bar(range(1, 4), pca.explained_variance_ratio_, alpha=0.7)
plt.xlabel("Principal Components")
plt.ylabel("Explained Variance Ratio")
plt.title("PCA Explained Variance")
plt.savefig(os.path.join(results_dir, "pca_explained_variance.png"))
plt.show()

# K-Means Clustering
# Find optimal clusters using the Elbow Method
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method for Optimal Clusters")
plt.savefig(os.path.join(results_dir, "elbow_method.png"))
plt.show()

# Apply K-Means with optimal clusters (choose based on elbow method)
optimal_clusters = 4  # Replace with the number of clusters from the elbow method
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
df_clean["Cluster"] = kmeans.fit_predict(scaled_data)

# Silhouette Score for clustering evaluation
sil_score = silhouette_score(scaled_data, kmeans.labels_)
print(f"Silhouette Score for optimal clustering: {sil_score}")

# Clustering Visualization (2D Projection using PCA)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=pca_df["PC1"], y=pca_df["PC2"], hue=df_clean["Cluster"], palette="Set2")
plt.title("Clusters in PCA Space")
plt.savefig(os.path.join(results_dir, "clusters_pca.png"))
plt.show()

# Save processed data with clusters
output_path = os.path.join(results_dir, "processed_with_clusters.csv")
df_clean.to_csv(output_path, index=False)

print(f"Multivariate analysis completed. Results saved in '{results_dir}'")
