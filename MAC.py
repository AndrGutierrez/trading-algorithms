import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy

# Read historical data from a CSV file or any other source
# Replace 'your_data.csv' with the path to your CSV file
data = pd.read_csv('data/ETH-USD-1d-2022-08-12T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]

# Define the Moving Average Crossover Strategy
class MovingAverageCrossover(Strategy):
    n1 = 5  # Short moving average window
    n2 = 20  # Long moving average window

    def init(self):
        self.short_mavg = self.I(talib.SMA, self.data.Close, self.n1)
        self.long_mavg = self.I(talib.SMA, self.data.Close, self.n2)

    def next(self):
        if self.short_mavg[-1] > self.long_mavg[-1] and self.short_mavg[-2] <= self.long_mavg[-2]:
            self.buy()
        elif self.short_mavg[-1] < self.long_mavg[-1] and self.short_mavg[-2] >= self.long_mavg[-2]:
            self.sell()

# Initialize and run the backtest
bt = Backtest(data, MovingAverageCrossover, cash=10000, commission=.002)
output = bt.run()
print(output)

# Plot the backtest results
bt.plot()