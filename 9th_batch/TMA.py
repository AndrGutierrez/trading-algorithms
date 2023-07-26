import backtesting
import talib
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Step 3: Define the TMA function

class TMAStrategy(Strategy):
    timeperiod1=10
    timeperiod2=20
    timeperiod3=30
    def init(self):
        self.sma1 = self.I(talib.SMA, self.data.Close, self.timeperiod1)
        self.sma2 = self.I(talib.SMA, self.data.Close, self.timeperiod2)
        self.sma3 = self.I(talib.SMA, self.data.Close, self.timeperiod3)

    def next(self):
        tma = (self.sma1[-1]+self.sma2[-1]+self.sma3[-1])/3
        if crossover(self.data.Close, tma):
            # self.sell(size=1)
            # self.buy(size=3)
            
            self.sell(size=1)
        elif crossover(tma, self.data.Close):
            # self.sell()
            # self.sell(size=1)

            self.buy()

# Step 5: Backtest the strategy using historical price data
if __name__ == '__main__':
    # Replace 'historical_price_data.csv' with your historical price data file path.
    # data = pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
    data = pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]

    bt = Backtest(data, TMAStrategy, cash=100000, commission=0.002)
    results = bt.run()

    print(results)

    # Generate a basic performance plot (requires matplotlib)
    bt.plot()
