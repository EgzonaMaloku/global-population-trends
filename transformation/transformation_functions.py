import pandas as pd
import numpy as np


def smoothing_by_moving_averages(df):
    return df.rolling(window=3, min_periods=1).mean()

def aggregate_urban_population(df):
    return df.groupby('Year')['Urban Population'].sum().reset_index()


def add_aggregated_urban_population(df):
    aggregated = aggregate_urban_population(df)
    aggregated.rename(columns={'Urban Population': 'World Urban Population'}, inplace=True)
    
    df = df.merge(aggregated, on='Year', how='left')
    
    return df


def normalize_by_min_max(df):
    return (df - df.min()) / (df.max() - df.min())

def normalize_by_z_score(df):
    print(df.std())
    return (df - df.mean()) / df.std()

def normalize_by_decimal_scaling(df):
    max_value = df.abs().max()
    j = len(str(int(max_value)))
    return df / (10**j)


def binning_by_boundaries(df, bins, labels):
    return pd.cut(df, bins=bins, labels=labels, right=False)