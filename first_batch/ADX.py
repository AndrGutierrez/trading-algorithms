import numpy as np
import pandas as pd
import talib as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

class ADXTrendStrengthStrategy(Strategy):
    adx_period = 14
    min_adx = 25
    trailing_stop_pct = 0.02

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        self.adx = self.I(ta.ADX, high, low, close, timeperiod=self.adx_period)
        self.close_shifted = self.data.Close.to_series().shift(1)



    def next(self):
        if not self.position:
            if self.adx[-1] > self.min_adx:
                if crossover(self.data.Close, self.close_shifted):
                    self.buy()
        else:
            if crossover(self.close_shifted, self.data.Close):
                self.sell()

if __name__ == '__main__':
    # Load historical data
    # data = pd.read_csv("your_historical_data_file.csv", parse_dates=True, index_col=0)
    # data = GOOG
    data = pd.read_csv("./data/UNI-USD-1d-2022-08-12T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]

    bt = Backtest(data, ADXTrendStrengthStrategy, cash=100000, commission=.001)
    stats = bt.run()

    print(stats)
    bt.plot()