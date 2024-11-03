import pandas as pd
from datetime import datetime
import numpy as np

def load_data(file_path):
    """Load the dataset and ensure correct data types."""
    data = pd.read_csv(file_path)
    data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
    data['Population'] = pd.to_numeric(data['Population'], errors='coerce')
    data['Median Age'] = pd.to_numeric(data['Median Age'], errors='coerce')
    return data

def remove_redundant_features(data, threshold=0.9):
    """
    Remove features that are highly correlated with each other.
    A feature is considered redundant if its correlation with another feature exceeds the threshold.
    """
    # Select only numeric columns for correlation calculation
    numeric_data = data.select_dtypes(include=[float, int])
    if numeric_data.empty:
        print("No numeric data found for correlation analysis.")
        return data, []  
    
    corr_matrix = numeric_data.corr().abs()

    # Get the upper triangle of the correlation matrix
    upper_triangle = np.triu(np.ones(corr_matrix.shape), k=1)
    upper_triangle_df = pd.DataFrame(upper_triangle, columns=corr_matrix.columns, index=corr_matrix.index)
    upper_triangle_values = corr_matrix.where(upper_triangle_df == 1)

    # Identify redundant features based on the threshold
    redundant_features = [
        column for column in upper_triangle_values.columns if any(upper_triangle_values[column] > threshold)
    ]

    # Return the data without redundant features and the list of removed features
    return data.drop(redundant_features, axis=1), redundant_features


def remove_irrelevant_features(data, irrelevant_columns):
    """
    Remove irrelevant features that do not contribute to the task.
    """
    return data.drop(irrelevant_columns, axis=1, errors='ignore')

def feature_selection(data):
    """Select key features and handle redundant ones."""
    selected_data = data[['country', 'Year', 'Population', 'Fertility Rate', 'Urban  Pop %', 'Migrants (net)', 'Median Age', 'Density (P/Km²)', 'DataType']].copy()
    selected_data.fillna(0, inplace=True)

    # Remove redundant features
    selected_data, removed_features = remove_redundant_features(selected_data)
    print(f"Removed features: {removed_features}")
    
    return selected_data


def feature_engineering(data):
    """Engineer new features to enhance analysis."""
    # Population growth rate
    data['Annual_Population_Growth'] = data.groupby('country')['Population'].pct_change().fillna(0)

    # Migration rate as a percentage of the population
    data['Migration_Rate'] = (data['Migrants (net)'] / data['Population']).fillna(0)

    # Categorize by median age
    data['Age_Category'] = data['Median Age'].apply(lambda x: 'Young' if x < 25 else ('Middle-Aged' if x <= 40 else 'Aging'))

    # Rolling average for Population with index alignment
    data['3_Year_Pop_Avg'] = data.groupby('country')['Population'].apply(lambda x: x.rolling(window=3, min_periods=1).mean()).reset_index(level=0, drop=True).fillna(0)

    return data

def save_to_csv(data, output_file_path):
    data.to_csv(output_file_path, index=False)
    print(f"File saved to {output_file_path}")

def main():
    file_path = '../data/dataset_02.csv'
    data = load_data(file_path)

    # Feature selection
    data = feature_selection(data)

    # Feature engineering
    data = feature_engineering(data)

    output_file_path = '../data/dataset_03.csv'
    save_to_csv(data, output_file_path)

if __name__ == "__main__":
    main()
