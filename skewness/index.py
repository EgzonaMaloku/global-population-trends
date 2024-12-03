import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import skew




def calculate_skewness(column, data):
    return skew(data[column].dropna())




# Function to plot distributions for the specified columns
def plot_distributions(columns, data):
    for col in columns:
        plt.figure(figsize=(10, 5))
        sns.histplot(data[col].dropna(), kde=True, bins=30, color="blue")
        plt.title(f"Distribution of {col} (Skewness: {skewness_values[col]:.2f})", fontsize=14)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()



# Function to calculate and annotate mean, median, and mode
def plot_distributions_with_stats(columns, data):
    for col in columns:
        skewness = calculate_skewness(col, data)

        plt.figure(figsize=(10, 5))
        column_data = data[col].dropna()
        
        # Calculate statistics
        mean_value = column_data.mean()
        median_value = column_data.median()
        mode_value = column_data.mode()[0] if not column_data.mode().empty else None
        
        # Plot histogram
        sns.histplot(column_data, kde=True, bins=30, color="blue")
        plt.axvline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
        plt.axvline(median_value, color='green', linestyle='--', label=f'Median: {median_value:.2f}')
        if mode_value is not None:
            plt.axvline(mode_value, color='purple', linestyle='--', label=f'Mode: {mode_value:.2f}')
        
        # Annotate plot
        plt.title(f"Distribution of {col} (Skewness: {skewness:.2f})", fontsize=14)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()


# Columns to visualize
columns_to_check = ["Annual_Population_Growth", "Migration_Rate", "Density (P/Km²)", "Fertility Rate", "Median Age", "Yearly  Change"]


data = pd.read_csv('../data/dataset_05.csv')
plot_distributions_with_stats(columns_to_check, data)
