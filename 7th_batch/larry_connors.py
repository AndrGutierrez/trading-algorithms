import backtesting
from backtesting import Strategy, Backtest
import talib
import pandas as pd

class MyStrategy(Strategy):
    timeperiod = 7
    def init(self):
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)  # Calculate SMA200
        self.lowest7 = self.I(talib.MIN, self.data.Low, timeperiod=self.timeperiod)  # Calculate lowest value in last 7 days
        self.high7 = self.I(talib.MAX, self.data.High, timeperiod=self.timeperiod)  # Calculate lowest value in last 7 days
        self.stop_loss = 0.1  # Set stop loss percentage

    def next(self):
        if self.data.Close[-1] > self.sma200[-1] and self.data.Close[-1] <= self.lowest7[-1]:
            self.buy()

        if self.data.Close[-1] >= self.high7:
            self.sell()

    def stop_loss_guard(self):
        self.sell(sl=self.data.Close[-1] * (1 - self.stop_loss))

# Load data
data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
data.columns=[column.capitalize() for column in data.columns]

# Initialize and run the strategy
bt= Backtest(data, MyStrategy, cash=100000, commission=0.002)
stats =bt.run()
print(stats)

# Evaluate and plot the results
bt.plot()
