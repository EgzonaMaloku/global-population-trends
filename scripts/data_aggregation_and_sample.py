import pandas as pd

def load_data(file_path):
    """Load the dataset."""
    return pd.read_csv(file_path)

def aggregate_country_data_by_type(data):
    """
    Aggregate statistics by country and DataType to compare Historical vs Forecasted data.
    """
    country_summary = data.groupby(['country', 'DataType']).agg({
        'Population': 'sum',
        'Migrants (net)': 'mean',
        'Median Age': 'mean',
        'Fertility Rate': 'mean',
        'Urban Population': 'sum'
    }).unstack().reset_index()

    # Flatten column levels created by unstacking
    country_summary.columns = [' '.join(col).strip() if col[1] else col[0] for col in country_summary.columns.values]

    print("Country-Level Aggregates by DataType (Historical vs Forecasted):")
    print(country_summary.head())
    return country_summary


def save_to_csv(data, output_file_path):
    """Save the DataFrame to a CSV file."""
    data.to_csv(output_file_path, index=False)
    print(f"File saved to {output_file_path}")

def sample_data_by_type(data, sample_size=50, random_state=42):
    """Sample equal amounts of Historical and Forecasted data."""
    historical_sample = data[data['DataType'] == 'Historical'].sample(n=sample_size, random_state=random_state)
    forecasted_sample = data[data['DataType'] == 'Forecasted'].sample(n=sample_size, random_state=random_state)
    
    sampled_data = pd.concat([historical_sample, forecasted_sample])
    print(f"Sampled Data (n={2 * sample_size}):")
    print(sampled_data.head())
    return sampled_data

def main(file_path):
    data = load_data(file_path)

    country_summary = aggregate_country_data_by_type(data)
    save_to_csv(country_summary, '../results/country_summary_by_datatype.csv')

    sampled_data = sample_data_by_type(data, sample_size=50)
    save_to_csv(sampled_data, '../processed/sampled_data.csv')

# Define the input file path and execute main function
file_path = '../processed/preprocessed_data.csv'
main(file_path)
