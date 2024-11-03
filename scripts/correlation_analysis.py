import pandas as pd

# Function to calculate specific correlations
def calculate_correlation(data, col1, col2):
    correlation = data[[col1, col2]].corr(method='pearson').iloc[0, 1]
    return correlation

# Load dataset for specific correlation calculations
preprocessed_data = pd.read_csv('../processed/preprocessed_data.csv')

# Calculate specific correlations
urban_correlation = calculate_correlation(preprocessed_data, 'Urban  Pop %', 'Urban Population')
yearly_change_correlation = calculate_correlation(preprocessed_data, 'Yearly %   Change', 'Yearly  Change')

print("Urban Pop % and Urban Population Correlation:", urban_correlation)
print("Yearly % Change and Yearly Change Correlation:", yearly_change_correlation)

# Load dataset for Rank correlation calculation
data = pd.read_csv('../data/dataset_03.csv')

# Define numeric columns explicitly for correlation, VIF, and PCA
numeric_columns = ['Population', 'Yearly %   Change', 'Yearly  Change', 'Migrants (net)', 
                   'Median Age', 'Fertility Rate', 'Density (P/Km²)', 'Urban  Pop %', 
                   'Urban Population', 'Rank']

data_numeric = data[numeric_columns]

# Calculate correlation for Rank with other features
correlations = data_numeric.corr()  # Default method is Pearson
print("\nCorrelation of Rank with other features:")
print(correlations['Rank'].drop('Rank'))


# Remove the Rank column and save the changes
data = data.drop(columns=['Rank'])
data.to_csv('../data/dataset_04.csv', index=False)