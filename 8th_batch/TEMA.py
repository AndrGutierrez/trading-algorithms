from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
from backtesting.lib import crossover
import talib

def vwma(prices, volumes, period):
    if len(prices) != len(volumes):
        raise ValueError("Length of prices and volumes should be equal.")
    
    if period > len(prices):
        raise ValueError("Period cannot be greater than the length of prices.")
    
    vwma_values = np.zeros(len(prices))
    
    for i in range(period - 1, len(prices)):
        price_sum = 0
        volume_sum = 0
        
        for j in range(i - period + 1, i + 1):
            price_sum += prices[j] * volumes[j]
            volume_sum += volumes[j]
        
        vwma_values[i] = price_sum / volume_sum
    
    return vwma_values

class Strat(Strategy):
    def init(self):
        self.vwma = self.I(vwma, self.data.Close, self.data.Volume, 20)
        self.tema = self.I(talib.TEMA, self.data.Close, 20)
    def next(self):
        # print(self.tema[-1], ", ", self.vwma[-1])
        if crossover(self.vwma, self.tema):
            self.buy()
        elif crossover(self.tema, self.vwma):
            self.sell()

if __name__ == '__main__':
    data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data.columns = [column.capitalize() for column in data.columns]
    bt = Backtest(data, Strat, cash=100000, commission=.002)
    output = bt.run()
    bt.plot()
