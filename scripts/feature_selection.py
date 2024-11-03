import pandas as pd

def load_data(file_path):
    """Load the entire dataset without dropping any columns."""
    data = pd.read_csv(file_path)
    data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
    data['Population'] = pd.to_numeric(data['Population'], errors='coerce')
    data['Median Age'] = pd.to_numeric(data['Median Age'], errors='coerce')
    return data

def feature_selection(data):
    """Select key features (subset of properties) for analysis."""
    selected_data = data[['country', 'Year', 'Population', 'Fertility Rate', 
                          'Urban  Pop %', 'Migrants (net)', 'Median Age', 
                          'Density (P/Km²)', 'DataType']].copy()
    selected_data.fillna(0, inplace=True)
    return selected_data

def feature_engineering(selected_data):
    """Engineer new properties to enhance analysis on the selected subset."""
    # Population growth rate
    selected_data['Annual_Population_Growth'] = selected_data.groupby('country')['Population'].pct_change().fillna(0)

    # Migration rate as a percentage of the population
    selected_data['Migration_Rate'] = (selected_data['Migrants (net)'] / selected_data['Population']).fillna(0)

    # Estimate dependency ratio (simple illustration)
    selected_data['Dependency_Ratio'] = selected_data['Population'] * (selected_data['Median Age'] / 100)
    selected_data['Dependency_Ratio'] = selected_data['Dependency_Ratio'] / (selected_data['Population'] - selected_data['Dependency_Ratio'])

    # Rolling average for Population with index alignment
    selected_data['3_Year_Pop_Avg'] = selected_data.groupby('country')['Population'].apply(lambda x: x.rolling(window=3, min_periods=1).mean()).reset_index(level=0, drop=True).fillna(0)

    return selected_data

def save_to_csv(original_data, selected_data, output_file_path):
    engineered_data = original_data.copy()
    for column in ['Annual_Population_Growth', 'Migration_Rate', 'Dependency_Ratio', '3_Year_Pop_Avg']:
        engineered_data[column] = selected_data[column]
    
    engineered_data.to_csv(output_file_path, index=False)
    print(f"File saved to {output_file_path}")

def main():
    file_path = '../data/dataset_02.csv'
    data = load_data(file_path)
    selected_data = feature_selection(data)
    selected_data = feature_engineering(selected_data)
    output_file_path = '../data/dataset_03.csv'
    save_to_csv(data, selected_data, output_file_path)

if __name__ == "__main__":
    main()
