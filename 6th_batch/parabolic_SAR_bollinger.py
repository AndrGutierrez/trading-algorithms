import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

class SARStrategy(Strategy):
    acc=2
    maximum=2
    def init(self):
        self.sar = self.I(talib.SAR, self.data.High, self.data.Low, acceleration=self.acc/100, maximum=self.maximum/10)
        self.bbolinger= self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)


    def next(self):
        # overbought = crossover(self.stoch_k, self.stoch_d)
        uptrend= crossover(self.data.Close, self.sar)
        downtrend=crossover(self.sar, self.data.Close)
        if uptrend or crossover(self.bbolinger, self.data.Close):
            self.buy(size=40, tp=self.data.Close[-1] * 1.2, sl=self.data.Close[-1] * 0.95)
            # self.buy()
        # else:
        #     self.sell()

# Load historical data
# Assuming 'high', 'low', and 'close' are the high, low, and closing prices of the asset

# data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
data=pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
# data=pd.read_csv('./data/ethereum/1d-2020-01-01T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
# Initialize and run the backtest
bt = Backtest(data, SARStrategy, cash=100_000)
bt.optimize(maximize="Equity Final [$]", acc=range(1, 10), maximum=range(1, 10))
# bt.run()

# Analyze the performance
bt.plot()
