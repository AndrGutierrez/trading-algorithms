import talib
import backtesting
import pandas as pd
from backtesting.lib import crossover

# Define the trading strategy
class EMACrossover(backtesting.Strategy):
    timeperiod1=7
    timeperiod2=17
    def init(self):
        self.ema7 = self.I(talib.EMA, self.data.Close, timeperiod=self.timeperiod1)
        self.ema17 = self.I(talib.EMA, self.data.Close, timeperiod=self.timeperiod2)

    def next(self):
        # if crossover(self.ema7, self.ema17):
        # if crossover(self.data.Close[-2], self.ema7[-1]) or crossover(self.data.Close[-1], self.ema17[-1]):
        if self.data.Close[-1] > self.ema7[-1] and self.data.Close[-1]> self.ema17[-1]:
            self.buy(tp=self.data.Close[-1]*1.05, sl=self.data.Close[-1]*0.90)
        elif self.ema7[-1] > self.data.Close[-1] and self.ema17[-1]> self.data.Close[-1]:
            # self.sell()
            pass
        # if self.ema7[-1] < self.ema17[-1] and self.ema7[-2] < self.ema17[-2]:
        #     self.buy()
        # else:
        #     self.sell()

# Load the data
# data=pd.read_csv('./data/bitcoin/1d-2020-01-01T00:00.csv')
# data=pd.read_csv('./data/ethereum/4h-2020-01-01T00:00.csv')
# data=pd.read_csv('./data/bitcoin/4h-2020-01-01T00:00.csv')
# data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
data=pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
data=data.dropna()
data.columns= [column.capitalize() for column in data.columns]

# Initialize and run the backtest
bt = backtesting.Backtest(data, EMACrossover, cash=100000)
bt.optimize(maximize="Equity Final [$]", timeperiod1=range(5, 20, 5), timeperiod2=range(10, 30, 5))
# bt.run()

# Generate and print the performance metrics
bt.plot()
