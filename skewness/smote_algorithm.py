import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

# Read dataset
data = pd.read_csv('../data/dataset_05.csv')

# Columns to analyze
columns_to_check = ["Annual_Population_Growth", "Migration_Rate", "Density (P/Km²)", "Fertility Rate", "Median Age", "Yearly  Change"]

# Ensure the columns exist in the dataset
missing_columns = [col for col in columns_to_check if col not in data.columns]
if missing_columns:
    print(f"Missing columns in dataset: {missing_columns}")
else:
    # Filter dataset for the specified columns
    filtered_data = data[columns_to_check]
    
    # Handle missing values
    filtered_data = filtered_data.fillna(filtered_data.mean())
    
    # Calculate Range, Variance, Mode, and Median
    range_values = filtered_data.max() - filtered_data.min()
    variance_values = filtered_data.var()
    mode_values = filtered_data.mode().iloc[0]  # Getting the first mode
    median_values = filtered_data.median()

    print("\nRange of Columns:")
    print(range_values)
    
    print("\nVariance of Columns:")
    print(variance_values)
    
    print("\nMode of Columns:")
    print(mode_values)
    
    print("\nMedian of Columns:")
    print(median_values)
    
    # Discretize the target column (Annual_Population_Growth) into categories
    bins = [-np.inf, 0, 1, np.inf]  # Define bins: <0 (low), 0-1 (medium), >1 (high)
    labels = ['Low Growth', 'Medium Growth', 'High Growth']
    filtered_data['Growth_Category'] = pd.cut(filtered_data['Annual_Population_Growth'], bins=bins, labels=labels)

    # SMOTE works on categorical target
    X = filtered_data.drop(columns=['Annual_Population_Growth', 'Growth_Category'])
    y = filtered_data['Growth_Category']
    
    # Apply SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Convert resampled data back to DataFrame
    resampled_data = pd.DataFrame(X_resampled, columns=X.columns)
    resampled_data['Growth_Category'] = y_resampled

    # Plot histograms and dot plots separately for "Before SMOTE" and "After SMOTE"
    def plot_hist_and_dots(columns, original_data, resampled_data):
        for col in columns:
            if col in original_data.columns and col in resampled_data.columns:
                plt.figure(figsize=(12, 12))

                # Histogram - Before SMOTE
                plt.subplot(2, 2, 1)
                sns.histplot(original_data[col].dropna(), kde=True, bins=30, color="blue", label="Before SMOTE")
                plt.title(f"Before SMOTE: {col} (Skewness: {original_data[col].skew():.2f})", fontsize=12)
                plt.xlabel(col, fontsize=10)
                plt.ylabel("Frequency", fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Histogram - After SMOTE
                plt.subplot(2, 2, 2)
                sns.histplot(resampled_data[col].dropna(), kde=True, bins=30, color="green", label="After SMOTE")
                plt.title(f"After SMOTE: {col} (Skewness: {resampled_data[col].skew():.2f})", fontsize=12)
                plt.xlabel(col, fontsize=10)
                plt.ylabel("Frequency", fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Dot Plot - Before SMOTE
                plt.subplot(2, 2, 3)
                plt.scatter(original_data[col], np.random.normal(0, 0.02, size=len(original_data[col])),
                            alpha=0.6, color="blue", label="Before SMOTE")
                plt.title(f"Dot Plot - Before SMOTE: {col}", fontsize=12)
                plt.xlabel(col, fontsize=10)
                plt.ylabel("Density (Dots)", fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Dot Plot - After SMOTE
                plt.subplot(2, 2, 4)
                plt.scatter(resampled_data[col], np.random.normal(0, 0.02, size=len(resampled_data[col])),
                            alpha=0.6, color="green", label="After SMOTE")
                plt.title(f"Dot Plot - After SMOTE: {col}", fontsize=12)
                plt.xlabel(col, fontsize=10)
                plt.ylabel("Density (Dots)", fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                plt.tight_layout()
                plt.show()

    # Plot histograms and dot plots for each column
    print("Histograms and Dot Plots Before and After SMOTE:")
    plot_hist_and_dots(
        [col for col in columns_to_check if col != 'Annual_Population_Growth'],  # Exclude the target column
        filtered_data,
        resampled_data,
    )

    # Visualize the distribution of Growth_Category after SMOTE (Dot Plot)
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=resampled_data['Growth_Category'].astype(str),
                    y=np.random.normal(0, 0.02, size=len(resampled_data['Growth_Category'])),
                    color="purple", alpha=0.6)
    plt.title("Distribution of Growth Category After SMOTE", fontsize=14)
    plt.xlabel("Growth Category", fontsize=12)
    plt.ylabel("Density (Dots)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
