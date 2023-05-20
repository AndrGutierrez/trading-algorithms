# Step 1: Install the required libraries
# pip install backtesting
# pip install TA-Lib

# Step 2: Import the necessary modules
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

# Step 3: Define the custom strategy class
class SMAPullbackStrategy(Strategy):
    n = 20  # 20-day Simple Moving Average

    def init(self):
        close = self.data.Close
        self.sma = self.I(talib.SMA, close, self.n)

    def next(self):
        price = self.data.Close[-1]
        sma = self.sma[-1]
        yesterday_low = self.data.Low[-2]
        stop_loss = yesterday_low
        take_profit = yesterday_low + 1.5 * (price - stop_loss)

        if self.position.is_long:
            if price <= stop_loss or price >= take_profit:
                self.position.close()

        elif price > sma:
            print(stop_loss, ", ", take_profit)
            try:
                self.buy(sl=stop_loss, tp=take_profit)
            except:
                pass

# Step 5: Test the strategy using historical data
if __name__ == '__main__':
    # Load historical data (example: OHLC data for Bitcoin/USD)
    data=GOOG

    # Run the backtest
    bt = Backtest(data, SMAPullbackStrategy, cash=10000, commission=.002)
    stats = bt.run()

    # Print the results
    print(stats)
    bt.plot()
