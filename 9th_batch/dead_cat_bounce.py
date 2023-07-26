import backtesting
import talib
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Define the trading strategy
class TrendChangeStrategy(Strategy):
    min_timeperiod=50
    def init(self):
        # Calculate MACD
        self.macd, self.signal, _ = self.I(talib.MACD, self.data.Close)
        self.bottom = self.I(talib.MIN, self.data.Close, timeperiod=self.min_timeperiod)
    def next(self):
        if crossover(self.signal, self.macd):
            self.buy(size=5, tp=self.data.Close[-1]*1.25)
            # self.buy()
        elif self.bottom[-1] >= self.data.Close[-1]:
            self.sell()

if __name__ == '__main__':      
    # Load historical price data (replace 'historical_price_data.csv' with your data file)
    data = pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]

    # Create and run the backtest
    bt = Backtest(data, TrendChangeStrategy, cash=100000, commission=.002)
    # bt = Backtest(data, StrongBearishTrendStrategy, cash=100000, commission=.002)
    # results = bt.run()
    results = bt.optimize(maximize="Equity Final [$]", min_timeperiod=range(50, 80, 5))

    # Print the results
    print(results)
    bt.plot()
