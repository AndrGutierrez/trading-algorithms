import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

class SARStrategy(Strategy):
    acc=2
    maximum=2
    def init(self):
        self.sar = self.I(talib.SAR, self.data.High, self.data.Low, acceleration=self.acc/100, maximum=self.maximum/10)
        self.stoch_k, self.stoch_d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close)


    def next(self):
        overbought = crossover(self.stoch_k, self.stoch_d)
        if crossover(self.data.Close, self.sar) and not overbought:
            self.buy(tp=self.data.Close[-1] * 1.05, sl=self.data.Close[-2] * 0.96)
        elif crossover(self.sar, self.data.Close) and overbought:
            self.sell()

# Load historical data
# Assuming 'high', 'low', and 'close' are the high, low, and closing prices of the asset

data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
# data=pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
# Initialize and run the backtest
bt = Backtest(data, SARStrategy, cash=100_000)
bt.optimize(maximize="Equity Final [$]", acc=range(1, 10), maximum=range(1, 10))
# bt.run()

# Analyze the performance
bt.plot()
