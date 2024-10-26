import pandas as pd

countries = ["Albania", "Croatia", "Egypt", "Germany", "United States", "United Arab Emirates", "Mexico", "Argentina", "China", "India"]
years = [1960, 1970, 1980, 1990, 2000, 2010, 2020]
indicators = ["SP.POP.TOTL", "SP.URB.TOTL"]

def filter_first_csv(file_path):
    df = pd.read_csv(file_path)
    filtered_df = df[(df['country'].isin(countries)) & (df['Year'].isin(years))].copy() 
    return filtered_df

def filter_second_csv(file_path):
    df = pd.read_csv(file_path, skiprows=4)
    filtered_df = df[(df['Country Name'].isin(countries)) & (df['Indicator Code'].isin(indicators))].copy() 
    
    year_columns = ['Country Name', 'Indicator Code'] + [str(year) for year in years]
    filtered_df = filtered_df[year_columns].copy() 
    
    melted_df = filtered_df.melt(id_vars=['Country Name', 'Indicator Code'], 
                                 var_name='Year', 
                                 value_name='Value').copy() 
    
    melted_df['Year'] = melted_df['Year'].astype(int)
    
    pop_totl_df = melted_df[melted_df['Indicator Code'] == 'SP.POP.TOTL'][['Country Name', 'Year', 'Value']].rename(columns={'Value': 'Population_Value'}).copy()
    urb_totl_df = melted_df[melted_df['Indicator Code'] == 'SP.URB.TOTL'][['Country Name', 'Year', 'Value']].rename(columns={'Value': 'Urban_Population_Value'}).copy()
    
    combined_df = pd.merge(pop_totl_df, urb_totl_df, on=['Country Name', 'Year'], how='inner')
    
    return combined_df

def difference_percentage(num1, num2):
    difference = abs(num1 - num2)
    
    average = (num1 + num2) / 2
    
    with pd.option_context('mode.chained_assignment', None): 
        percentage_difference = (difference / average).replace({0: None}) * 100
    
    return percentage_difference

def create_combined_csv(file_first_csv, file_second_csv, output_file):
    first_csv_data = filter_first_csv(file_first_csv)
    second_csv_data = filter_second_csv(file_second_csv)
    
    merged_df = pd.merge(
        first_csv_data,
        second_csv_data,
        left_on=['country', 'Year'],
        right_on=['Country Name', 'Year'],
        how='inner'
    )
    
    final_df = merged_df[['country', 'Year', 'Population', 'Population_Value', 'Urban Population', 'Urban_Population_Value']]
    final_df.columns = ['Country', 'Year', 'Population', 'WorldBank_Population', 'Urban Population', 'WorldBank_Urban_Population']
    
    final_df['Population'] = pd.to_numeric(final_df['Population'], errors='coerce')
    final_df['WorldBank_Population'] = pd.to_numeric(final_df['WorldBank_Population'], errors='coerce')
    final_df['Urban Population'] = pd.to_numeric(final_df['Urban Population'], errors='coerce')
    final_df['WorldBank_Urban_Population'] = pd.to_numeric(final_df['WorldBank_Urban_Population'], errors='coerce')
    
    final_df.loc[:, 'Population Difference'] = final_df['Population'] - final_df['WorldBank_Population']
    final_df.loc[:, 'Population Difference %'] = difference_percentage(final_df['Population'], final_df['WorldBank_Population']) 
    final_df.loc[:, 'Urban Population Difference'] = final_df['Urban Population'] - final_df['WorldBank_Urban_Population']
    final_df.loc[:, 'Urban Population Difference %'] = difference_percentage(final_df['Urban Population'], final_df['WorldBank_Urban_Population']) 
    
    final_df.to_csv(output_file, index=False)
    print(f"Combined CSV file created at: {output_file}")

file_first_csv = '../main_dataset.csv'    
file_second_csv = 'worldbank_dataset.csv'  
output_file = 'compared_with_worldbank.csv'       

create_combined_csv(file_first_csv, file_second_csv, output_file)
