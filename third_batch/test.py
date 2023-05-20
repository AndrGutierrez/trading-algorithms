from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import pandas as pd

class MovingAverageStrategy(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        self.sma1 = self.I(pd.Series.rolling, self.data.Close, self.n1).mean()
        self.sma2 = self.I(pd.Series.rolling, self.data.Close, self.n2).mean()

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

bt = Backtest(GOOG, MovingAverageStrategy, cash=10000, commission=.002)
stats = bt.run()
bt.plot()
