from backtesting import Backtest, Strategy
import talib
import numpy as np
import pandas as pd

# Define the trading strategy
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, cross

class NPOCStrategy(Strategy):
    def init(self):
        self.nPOC_period = 20  # Number of periods to calculate nPOC
        self.fibonacci_levels = [0.618, 0.786]  # Fibonacci retracement levels
        self.long_trade = False
        self.short_trade = False

    def next(self):
        # Calculate negative point of control zone (nPOC)
        nPOC = talib.VALUEAREA(self.data.High, self.data.Low, self.data.Close, self.nPOC_period)[0]

        # Check if price enters nPOC zone
        if self.data.Close[-1] < nPOC:
            # Calculate Fibonacci retracement levels from the current price
            current_price = self.data.Close[-1]
            price_range = self.data.High[-self.nPOC_period:].max() - self.data.Low[-self.nPOC_period:].min()
            fibonacci_levels_prices = [current_price - level * price_range for level in self.fibonacci_levels]

            # Check if price crosses golden pocket levels (between 0.618 and 0.786)
            if crossover(self.data.Close, fibonacci_levels_prices[0]) and self.long_trade == False:
                self.buy()
                self.long_trade = True
                self.short_trade = False
            elif crossover(fibonacci_levels_prices[1], self.data.Close) and self.short_trade == False:
                self.sell()
                self.long_trade = False
                self.short_trade = True

if __name__ == "__main__":
    data=pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt=Backtest(data,NegativePOCStrategy,cash=100000,commission=.002)
    stats=bt.run()
    bt.plot()
