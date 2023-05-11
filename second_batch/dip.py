import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

# Load your data as a Pandas DataFrame
class DipBuyStrategy(Strategy):
    buy_dips = [0.95, 0.90]  # 5% and 10% dips
    profit_target = 1.03  # 3% gain

    def init(self):
        # Compute the buy and sell levels for each candle
        self.buy_levels = [self.data.Close * dip for dip in self.buy_dips]
        self.sell_level = self.data.Close * self.profit_target

    def next(self):
        # Determine whether to buy or sell at the current bar

        # If we don't have a position, look for a buy opportunity
        if not self.position:
            for buy_level in self.buy_levels:
                if self.data.Close[-1] <= buy_level[-1]:
                    self.buy()
                    break
        # If we have a position, look for a sell opportunity
        else:
            if self.data.Close[-1] >= self.sell_level[-1]:
                self.position.close()


data = GOOG
data= pd.read_csv('./data/UNI-USD-1d-2022-04-17T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]
bt = Backtest(data, DipBuyStrategy, cash=10000, commission=.002)
# optimization = bt.optimize(
#     buy_dips=([0.95, 0.90], [0.93, 0.87], [0.90, 0.80]),
#     profit_target=(1.03, 1.05, 1.10),
#     maximize='Equity Final [$]',
#     # constraint=lambda p: p.profit_target > 1 + (min(p.buy_dips) - 1) * 0.5
# )
bt.run()
bt.plot()
