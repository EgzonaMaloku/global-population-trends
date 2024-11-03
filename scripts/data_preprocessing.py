import pandas as pd
import numpy as np

def set_column_data_types(data):
    """Set data types for specific columns and clean percentage columns."""
    # Convert population and integer columns
    data['Population'] = data['Population'].astype(int)
    data['Year'] = data['Year'].astype(int)
    data['Density (P/Km²)'] = data['Density (P/Km²)'].astype(int)
    data['World Population'] = data['World Population'].astype(int)
    data['Rank'] = data['Rank'].astype(int)
    
    # Clean percentage columns and convert to float
    if 'Yearly %   Change' in data.columns:
        data['Yearly %   Change'] = data['Yearly %   Change'].str.replace('%', '').replace('N.A.', np.nan).astype(float) / 100
    if 'Yearly  Change' in data.columns:
        data['Yearly  Change'] = data['Yearly  Change'].replace('N.A.', np.nan).astype(float)
    
    data['Urban  Pop %'] = data['Urban  Pop %'].str.replace('%', '').replace('N.A.', np.nan).astype(float) / 100
    data["Country's Share of  World Pop"] = data["Country's Share of  World Pop"].str.replace('%', '').replace('N.A.', np.nan).astype(float) / 100
    
    # Replace empty strings or spaces with NaN for certain columns
    data['Migrants (net)'] = data['Migrants (net)'].replace(' ', np.nan).astype(float)
    data['Median Age'] = data['Median Age'].replace(' ', np.nan).astype(float)
    data['Fertility Rate'] = data['Fertility Rate'].replace(' ', np.nan).astype(float)
    data['Urban Population'] = pd.to_numeric(data['Urban Population'].replace(' ', np.nan), errors='coerce')
    
    # Set object types for string columns
    data['country'] = data['country'].astype(str)
    data['DataType'] = data['DataType'].astype(str)
    
    return data

def remove_duplicates(data):
    # Sort data to prioritize rows with fewer missing values
    data_sorted = data.sort_values(by=data.columns.tolist(), ascending=False, na_position='last')
    
    initial_duplicate_count = data_sorted.duplicated(subset=['country', 'Year', 'DataType']).sum()
    print(f"Number of duplicates before removal: {initial_duplicate_count}")
    
    data_no_duplicates = data_sorted.drop_duplicates(subset=['country', 'Year', 'DataType'], keep='first')
    
    final_duplicate_count = data_no_duplicates.duplicated(subset=['country', 'Year', 'DataType']).sum()
    print(f"Number of duplicates after removal: {final_duplicate_count}")
    
    return data_no_duplicates

def fill_missing_values(data):
    """Fill missing values based on column and group level logic, with consideration for DataType."""
    
    # Columns that will be filled with the median by 'country' and 'DataType' to avoid mixing Forecasted and Historical data
    datatype_fill_columns = ['Migrants (net)', 'Median Age', 'Fertility Rate', 'Urban  Pop %', 'Urban Population']
    
    # 1. Fill columns with median by 'country' and 'DataType'
    for col in datatype_fill_columns:
        data[col] = data.groupby(['country', 'DataType'])[col].transform(lambda x: x.fillna(x.median()) if x.notnull().any() else x)
    
    # 2. Estimate 'Urban Population' based on 'Population' and 'Urban Pop %' if still missing
    data['Urban Population'] = data['Urban Population'].fillna(data['Population'] * data['Urban  Pop %'])
    
    # 3. Forward-fill and backward-fill within each 'country' and 'DataType' for remaining missing values
    data[datatype_fill_columns] = data.groupby(['country', 'DataType'])[datatype_fill_columns].ffill().bfill()
    
    return data

