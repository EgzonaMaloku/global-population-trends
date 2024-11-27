import numpy as np
import matplotlib.pyplot as plt


numeric_cols = data.select_dtypes(include=[np.number])

# Z-Score Method
z_scores = (numeric_cols - numeric_cols.mean()) / numeric_cols.std()
outliers_zscore = z_scores[(np.abs(z_scores) > 3).any(axis=1)]

print("Outliers detected using Z-Score:")
print(outliers_zscore)

# IQR Method
Q1 = numeric_cols.quantile(0.25)
Q3 = numeric_cols.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = numeric_cols[(numeric_cols < lower_bound) | (numeric_cols > upper_bound)].dropna(how='all')

print("\nOutliers detected using IQR:")
print(outliers_iqr)

# Visualization
plt.figure(figsize=(10, 6))
numeric_cols.boxplot()
plt.title("Boxplot for Outlier Detection")
plt.xticks(rotation=45)
plt.show()
