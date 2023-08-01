import backtesting
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import numpy as np

PEAK, VALLEY = 1, -1

def _identify_initial_pivot(X, up_thresh, down_thresh):
    x_0 = X[0]
    max_x = x_0
    max_t = 0
    min_x = x_0
    min_t = 0
    up_thresh += 1
    down_thresh += 1

    for t in range(1, len(X)):
        x_t = X[t]

        if x_t / min_x >= up_thresh:
            return VALLEY if min_t == 0 else PEAK

        if x_t / max_x <= down_thresh:
            return PEAK if max_t == 0 else VALLEY

        if x_t > max_x:
            max_x = x_t
            max_t = t

        if x_t < min_x:
            min_x = x_t
            min_t = t

    t_n = len(X)-1
    return VALLEY if x_0 < X[t_n] else PEAK

def calculate_zigzag(close, high, low, up_thresh, down_thresh):
    if down_thresh > 0:
        raise ValueError('The down_thresh must be negative.')

    initial_pivot = _identify_initial_pivot(close, up_thresh, down_thresh)

    t_n = len(close)
    pivots = np.zeros(t_n, dtype='i1')
    pivots[0] = initial_pivot

    up_thresh += 1
    down_thresh += 1

    trend = -initial_pivot
    last_pivot_t = 0
    last_pivot_x = close[0]
    
    for t in range(1, len(close)):
        if trend == -1:
            x = low[t]
            r = x / last_pivot_x
            
            if r >= up_thresh:
                pivots[last_pivot_t] = trend
                trend = 1
                last_pivot_x = high[t]
                last_pivot_t = t
            elif x < last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t
        else:
            x = high[t]
            r = x / last_pivot_x
            
            if r <= down_thresh:
                pivots[last_pivot_t] = trend
                trend = -1
                last_pivot_x = low[t]
                last_pivot_t = t
            elif x > last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t

    if last_pivot_t == t_n-1:
        pivots[last_pivot_t] = trend
    elif pivots[t_n-1] == 0:
        pivots[t_n-1] = trend

    return pivots

class ZigZagStrategy(Strategy):
    
    signal_triggered = False
    retracement_threshold=0.015
    def init(self):
        # Calculate zigzag trendlines
        self.swing_high_low = self.I(calculate_zigzag, self.data.Close, self.data.High, self.data.Low, self.retracement_threshold, -self.retracement_threshold)
    def next(self):

        if self.swing_high_low[-1] == 1:
            # Check for a bullish reversal and enter a long position
            if self.data.Close[-1] <= self.data.High[-1] * (1 - self.retracement_threshold):
                self.buy(size=2)
                # self.buy()

        elif self.swing_high_low[-1] == -1:
            # Check for a bearish reversal and enter a short position
            if self.data.Close[-1] >= self.data.Low[-1] * (1 + self.retracement_threshold):
                self.sell(size=1)
                # self.sell()
                # self.sell(size=5)

if __name__=="__main__":
    data = pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    # data=data.dropna()
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(
        data,
        ZigZagStrategy,
        cash=100000,
        commission=0.002,
    )
    stats= bt.run()
    print(stats)
    bt.plot()
