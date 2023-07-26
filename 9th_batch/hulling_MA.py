from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np
import talib

def hull_moving_average(data, window):
    weighted_data = 2 * pd.Series(data).ewm(span=window // 2).mean() - pd.Series(data).ewm(span=window).mean()
    hull_moving_avg = pd.Series(weighted_data).ewm(span=int(np.sqrt(window))).mean()
    return hull_moving_avg

class HullingStrategy(Strategy):
    timeperiod=50
    def init(self):
        # Define the indicators
        self.hma = self.I(hull_moving_average, self.data.Close, self.timeperiod)

    def next(self):
        if crossover(self.data.Close, self.hma):
            self.buy(sl=self.data.Close[-1] * 0.95, tp=self.data.Close[-1]*1.05)
        elif not self.position:
                self.sell()

if __name__ == "__main__":
    data= pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt= Backtest(data, HullingStrategy, cash=100000,commission=0.001)
    # stats= bt.run()
    stats= bt.optimize(maximize="Equity Final [$]", timeperiod=range(50, 70, 5))
    bt.plot()
