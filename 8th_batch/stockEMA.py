import talib
from backtesting import Strategy, Backtest
import numpy as np
import pandas as pd
from backtesting.lib import crossover


def calculate_acceleration_deceleration(data):
    acceleration = []
    deceleration = []

    for i in range(len(data)):
        if i < 2:
            acceleration.append(0)
            deceleration.append(0)
        else:
            current = data[i]
            previous = data[i-1]
            pre_previous = data[i-2]

            if current > previous > pre_previous:
                acceleration.append(current - previous)
                deceleration.append(0)
            elif current < previous < pre_previous:
                deceleration.append(previous - current)
                acceleration.append(0)
            else:
                acceleration.append(0)
                deceleration.append(0)

    return acceleration, deceleration

def check_uptrend(accelerator_data):
    if len(accelerator_data) < 3:
        return False

    recent_bars = accelerator_data[-3:]

    if recent_bars[0] > recent_bars[1] > recent_bars[2] and recent_bars[2] > 0:
        return True

    return False

class StockEMA(Strategy):
    timeperiod=34
    def init(self):
        self.acceleration=self.I(calculate_acceleration_deceleration, self.data.Close)
        self.ema=self.I(talib.EMA, self.data.Close, timeperiod=self.timeperiod)
        self.stochasticRSI=self.I(talib.STOCHRSI, self.data.Close)

    def next(self):
        # if self.stochasticRSI<=0:
        if crossover(self.data.Close, self.ema) or self.stochasticRSI[-1]<0 and check_uptrend(self.acceleration):
            self.buy(size=5, tp=self.data.Close[-1]*1.5, sl=self.data.Close[-1]*0.95)
if __name__=="__main__":
    # data = pd.read_csv("./data/ethereum/4h-2021-07-01T00:00.csv")
    data = pd.read_csv("./data/bitcoin/4h-2021-07-01T00:00.csv")
    data.columns = [column.capitalize() for column in data.columns]
    data = data.dropna()
    bt= Backtest(data, StockEMA, cash=100000, commission=.002)
    stats=bt.optimize(maximize='Equity Final [$]', timeperiod=range(10, 50, 5))
    print(stats)
    bt.plot()
