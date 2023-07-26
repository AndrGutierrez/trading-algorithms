import backtesting
import talib
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
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

class RVIStrategy(Strategy):
    rvi_period1=4
    rvi_period2=10
    rvi_treshold=30
    def init(self):
        # Calculate the 10MA and 4MA for RVI
        self.rvi_10 = self.I(calculate_rvi, data, period=self.rvi_period2)
        self.rvi_4 = self.I(calculate_rvi, data, period=self.rvi_period1)

    def next(self):
        # if self.position:
        if crossover(self.rvi_10, self.rvi_4):
            self.sell()
            # If no position, check for entry conditions
        elif self.rvi_10[-1] < self.rvi_treshold:  # Adjust the oversold threshold as needed
                # Entry for long position if RVI is below 30 (oversold)
                self.buy(sl=self.data.Close[-1]*.98, tp=self.data.Close[-1]*1.07)


# Load historical price data (replace 'price_data.csv' with your data file)
if __name__ == "__main__":
    # data = pd.read_csv('./data/bitcoin/5m-2023-04-01T00:00.csv')
    data = pd.read_csv('./data/ethereum/5m-2023-04-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]


    # Run the backtest
    bt = Backtest(data, RVIStrategy, cash=100000, commission=.002)
    # output = bt.run()
    output = bt.optimize(maximize="Equity Final [$]", rvi_period1=range(3, 9), rvi_period2=range(10,20,2), rvi_treshold=range(25, 40, 5))

    # Evaluate the backtest results 
    print(output)
    bt.plot()
