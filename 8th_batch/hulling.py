from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd
import numpy as np


def hull_moving_average(data, window):
    weighted_data = 2 * pd.Series(data).ewm(span=window // 2).mean() - pd.Series(data).ewm(span=window).mean()
    hull_moving_avg = pd.Series(weighted_data).ewm(span=int(np.sqrt(window))).mean()
    return hull_moving_avg

class HullingMovingAverageStrategy(Strategy):
    hma1 = 20
    hma2=100
    def init(self):
        # Define the indicators
        self.hma_20 = self.I(hull_moving_average, self.data.Close, self.hma1)
        self.hma_100 = self.I(hull_moving_average, self.data.Close, self.hma2)

    def next(self):
        # Check for a buy signal
        # if self.hma_20[-1] > self.hma_100[-1] and self.hma_20[-2] <= self.hma_100[-2]:
        if crossover(self.hma_20, self.hma_100):
            self.buy()
            if self.data.Low[-2] < self.data.Close[-1]:
                # self.buy(size=buy_size, sl=self.data.Low[-2]*0.97)
                self.buy(sl=self.data.Low[-1])
            else:
                # self.buy(size=buy_size)
                self.buy()

        # Check for a sell signal
        # elif self.hma_20[-1] < self.hma_100[-1] and self.hma_20[-2] >= self.hma_100[-2]:
        # elif crossover(self.hma_100, self.hma_20):
        elif not self.position:
                self.sell()

# Load the data
if __name__ == '__main__':
    data=pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    # Create an instance of the strategy
    bt = Backtest(data, HullingMovingAverageStrategy, cash=100000, commission=.002)

    # Run the backtest
    # result = bt.run()
    result = bt.optimize(hma1=range(10, 50, 5), hma2=range(50, 200, 25), maximize='Equity Final [$]')
    print(result)
    bt.plot()
