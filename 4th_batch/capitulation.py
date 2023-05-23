from backtesting import Strategy, Backtest
from backtesting.lib import crossover
from backtesting.test import GOOG
from talib import SMA
import pandas as pd

class MyStrategy(Strategy):

    def init(self):
        self.esperando_liquidacion = False
        self.sma = self.I(SMA, self.data.Close, 50)
        
    def next(self):
        if self.data.Close[-1] < 1.3*self.data.Open[-1]:
            self.esperando_liquidacion = True
        if self.esperando_liquidacion and self.data.Volume[-1] > 1.2*self.data.Volume[-2]:
            self.buy()
            self.esperando_liquidacion = False
        if crossover(self.data.Close, self.sma):
            self.sell()

# data=GOOG
data= pd.read_csv('./data/BTC-USD-1d-2022-06-04T00:00.csv')
data.columns = [column.capitalize() for column in data.columns]
bt = Backtest(data, MyStrategy, cash=100000)
output = bt.run()
bt.plot()
