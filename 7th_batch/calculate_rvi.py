import pandas as pd
def calculate_rvi(data, period=14):
    # Convert data to pandas DataFrame (if not already)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    # Calculate the difference between closing prices
    data['Close_diff'] = data['Close'].diff()
    
    # Calculate the smoothed sum of up and down closing price differences
    data['Up_sum'] = data['Close_diff'].apply(lambda x: x if x > 0 else 0).rolling(period).sum()
    data['Down_sum'] = data['Close_diff'].apply(lambda x: abs(x) if x < 0 else 0).rolling(period).sum()
    
    # Calculate the RVI indicator
    data['RVI'] = data['Up_sum'] / (data['Up_sum'] + data['Down_sum'])
    
    return data['RVI']
