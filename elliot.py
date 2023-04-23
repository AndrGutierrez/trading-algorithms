import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

def moving_average_cross(price_data, short_period, long_period):
    short_ma = talib.SMA(price_data, timeperiod=short_period)
    long_ma = talib.SMA(price_data, timeperiod=long_period)
    cross_above = short_ma > long_ma
    cross_below = short_ma < long_ma
    return cross_above, cross_below

class ElliottWaveStrategy(Strategy):
    def init(self):
        self.price = self.data.Close
        self.cross_above, self.cross_below = moving_average_cross(self.price, 20, 50)
        self.in_position = False

    def next(self):
        current_index = len(self.price) - 1

        # Enter a long position when short MA crosses above long MA
        if self.cross_above[current_index] and not self.in_position:
            self.buy()
            self.in_position = True

        # Exit the long position when short MA crosses below long MA
        elif self.cross_below[current_index] and self.in_position:
            self.sell()
            self.in_position = False

data = pd.DataFrame(GOOG)
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

def moving_average_cross(price_data, short_period, long_period):
    short_ma = talib.SMA(price_data, timeperiod=short_period)
    long_ma = talib.SMA(price_data, timeperiod=long_period)
    cross_above = short_ma > long_ma
    cross_below = short_ma < long_ma
    return cross_above, cross_below

class ElliottWaveStrategy(Strategy):
    def init(self):
        self.price = self.data.Close
        self.cross_above, self.cross_below = moving_average_cross(self.price, 20, 50)
        self.in_position = False

    def next(self):
        current_index = len(self.price) - 1

        # Enter a long position when short MA crosses above long MA
        if self.cross_above[current_index] and not self.in_position:
            self.buy()
            self.in_position = True

        # Exit the long position when short MA crosses below long MA
        elif self.cross_below[current_index] and self.in_position:
            self.sell()
            self.in_position = False

data = pd.read_csv('./data/ETH-USD-5m-2023-04-06T00:00.csv', index_col=0, parse_dates=True)
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, ElliottWaveStrategy, cash=10000, commission=.002)
stats = bt.run()
print(stats)