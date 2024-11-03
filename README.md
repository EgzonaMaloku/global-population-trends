# Global Population and Forecast Analysis

This project combines historical and forecasted population data for different countries, to analyze trends like population growth, urbanization, demographic changes, and migration.

## Key Features

### Historical vs. Forecasted Data:
Each row is labeled as either "Historical" or "Forecasted" to help compare past data with future predictions.

### Types of Analysis:

- **Population Growth**: Compare how population growth (percentage change and absolute numbers) evolved in the past vs. predictions for the future.
- **Urbanization**: Analyze how urban populations have grown historically and what is projected for the future.
- **Demographic Shifts**: Examine changes in median age, fertility rates, and other factors over time.
- **Migration Peaks and Declines**: Look for years with significant migration spikes or drops.
- **Future Projections**: Analyze which countries are predicted to see major migration changes in the coming years.

## Visualizing Trends:
Use charts (e.g., line charts, bar charts) to visualize trends from 1950 to 2040, comparing past data with future projections.

### Example Analysis Questions:

- **Are global population growth rates expected to decline in the future compared to historical rates?**
- **How does the future forecast for urbanization compare to historical trends?**
- **Which countries will see the largest changes in population size and structure over the next few decades?**
- **What regions are expected to experience the largest migration inflows or outflows?**


## Data Processing Workflow

The following steps outline the data processing, type conversions, and cleaning operations performed on the dataset.

### 1. Data Loading

Data is loaded from the `original_dataset.csv` file, with the columns verified before proceeding.

### 2. Data Type Conversion

To ensure consistency, appropriate data types were assigned to specific columns:

- **Integer Columns**:
  - `Population`
  - `Year`
  - `Yearly Change`
  - `Density (P/Km²)`
  - `World Population`
  - `Rank`

- **Float Columns**:
  - `Yearly % Change`: Cleaned by removing `%` symbols and converted to decimal format (e.g., `1.30%` becomes `0.013`).
  - `Urban Pop %`: Cleaned similarly by removing `%` symbols and converting to decimal.
  - `Country's Share of World Pop`: Cleaned by removing `%` symbols and converted to decimal.
  - `Migrants (net)`
  - `Median Age`
  - `Fertility Rate`
  - `Urban Population`

- **String Columns**:
  - `country`
  - `DataType`

### 3. Data Cleaning

To prepare the dataset for analysis, several cleaning operations were performed:

1. **Remove Symbols**: In columns like `Yearly % Change`, `Urban Pop %`, and `Country's Share of World Pop`, `%` symbols were removed, and the values were converted to decimal format.
2. **Handle Missing Values**: Placeholder values like `"N.A."` and empty strings were replaced with `NaN`, allowing for consistent handling of missing values across the dataset.
3. **Replace Empty Strings with NaN**: For columns that may have contained empty strings or spaces (e.g., `Migrants (net)`, `Median Age`, `Fertility Rate`, and `Urban Population`), these were replaced with `NaN` to ensure uniformity in missing value treatment.

### 4. Duplicate Removal

Duplicates were identified and removed based on the `country`, `DataType` and `Year` columns, ensuring unique time-series data for each country. This process helps prevent duplication in historical and forecasted data analysis.

### 5. Missing Value Handling

Missing values were addressed as follows:

1. **Country and DataType Level**: Median values were calculated for each column by grouping by `country` and `DataType` to avoid mixing "Historical" and "Forecasted" data.
2. **Urban Population Estimate**: For entries where `Urban Population` was missing, values were estimated by calculating `Population * Urban Pop %`.
3. **Forward and Backward Fill**: Missing values within each `country` and `DataType` group were forward- and backward-filled for columns where this approach was feasible.
4. **Global Median Imputation**: For any remaining missing values, global median values were used as a last resort.


### 6. Data Aggregation 
##### Country-Level Aggregation

Country-level aggregation groups data by `country` and `DataType` to allow for comparisons between historical and forecasted data for each country.

**Aggregated Metrics:**
- **Population**: Total population for each country and DataType.
- **Migrants (net)**: Average migration values.
- **Median Age**: Average median age.
- **Fertility Rate**: Average fertility rate.
- **Urban Population**: Summed urban population for each country and DataType.

**Example Output:**
| country   | DataType   | Population | Migrants (net) | Median Age | Fertility Rate | Urban Population |
|-----------|------------|------------|----------------|------------|----------------|-------------------|
| Albania   | Historical | 48,032,715 | -16,714.89     | 27.42      | 3.23           | 22,098,759       |
| Albania   | Forecasted | 18,818,407 | -10,357.14     | 43.19      | 1.62           | 14,196,195       |

### 7.Sampling

Sampling is used to select a representative subset of data, ensuring a balance between Historical and Forecasted records, which aids in effective and manageable analysis.

**Sampling Method:**
- **Equal Sampling by DataType**: Randomly selects an equal number of Historical and Forecasted records (e.g., 50 each) to create a balanced sample.

**Example Output:**
| country    | Year | Population | DataType   |
|------------|------|------------|------------|
| Albania    | 2017 | 2,876,664  | Historical |
| Albania    | 2035 | 424,537    | Forecasted |