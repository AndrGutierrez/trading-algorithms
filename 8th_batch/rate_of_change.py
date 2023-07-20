from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import numpy as np
import pandas as pd
import talib

def calculate_candle_size(open, close, timeperiod):
    average_sizes = []
    for i in range(len(open)):
        sizes=[]
        start = i - timeperiod 
        if start < 0:
            start=0
        close_frame = close[start:i]
        open_frame = open[start:i]
        for j in range(len(open_frame)):
            candle_size = abs(close_frame[j]-open_frame[j])  
            sizes.append(candle_size)
        average_candle_size = np.mean(sizes) 
        average_sizes.append(average_candle_size)
    return average_sizes


class RateOfChange(Strategy):
    sma_period = 4
    def init(self):
        # Calculate the average size of the candlesticks in the past 100 days
        self.average_candle_size =self.I(calculate_candle_size, self.data.Open, self.data.Close, 150)
        self.sma = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period)

    def next(self):
        bar_size= self.data.Close[-1]-self.data.Open[-1]
        if abs(bar_size) >= self.average_candle_size * 1.5:
            if bar_size < 0 or crossover(self.data.Close, self.sma):
                self.buy()
            elif bar_size > 0:
                self.sell(size=2)

if __name__=='__main__':
    data= pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data.columns = [column.capitalize() for column in data.columns]
    bt= Backtest(data, RateOfChange, cash=100000, commission=.002)
    # stats=bt.optimize(maximize="Equity Final [$]", sma_period=range(4, 10))
    stats=bt.run()
    print(stats)
    bt.plot()
