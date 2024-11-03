import pandas as pd

def sample_data(data, sample_size=500, random_state=42):
    """Randomly samples data by DataType for analysis."""
    historical_sample = data[data['DataType'] == 'Historical'].sample(n=sample_size, random_state=random_state)
    forecasted_sample = data[data['DataType'] == 'Forecasted'].sample(n=sample_size, random_state=random_state)
    
    sampled_data = pd.concat([historical_sample, forecasted_sample])
    return sampled_data
