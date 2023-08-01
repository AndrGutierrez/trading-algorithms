import talib
from backtesting import Backtest, Strategy
import pandas as pd

class NPOCStrategy(Strategy):
    nPOC_period = 20  # Number of periods to calculate nPOC
    def init(self):
        self.threshold = 0.95  # Price threshold to maintain a price lower than POC
        self.fib_levels = [0.236, 0.382, 0.618]  # Fibonacci retracement levels
        self.stop_loss = 0.02  # 2% stop loss level
        self.take_profit = 0.03  # 3% take profit level
        
        # Calculate nPOC using TALib
        self.nPOC = self.I(talib.MIDPOINT, self.data.Close, self.nPOC_period)
        
    def next(self):
        high = self.data.High[-1]
        low = self.data.Low[-1]

        # Calculate Fibonacci retracement levels
        fib_retracements = [high - level * (high - low) for level in self.fib_levels]

        # Calculate the Golden Pocket level (61.8%)
        golden_pocket = fib_retracements[-1]
        # Enter a position if the asset enters the nPOC zone and price is lower than POC
        if self.data.Close[-1] < self.nPOC[-1] and self.data.Close[-2] < self.nPOC[-2] and self.data.Close[-1] < self.data.Close[-2] and self.data.Close[-1] >= golden_pocket:
            # self.buy(size=1)
            # self.buy(sl=self.data.Close[-1]* 0.98, tp=self.data.Close[-1]* 1.03, size=1)
            self.buy()
        

        # Exit the position if price reaches the threshold
        elif self.data.Close[-1] > self.data.Close[-2] * self.threshold:
            # self.sell(size=1)
            # self.sell(size=1)
            self.sell(size=5)




# Load the historical price data
# Assuming you have a CSV file containing OHLC data with a column named 'Close'
data = pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]

# Initialize and run the backtest
bt = Backtest(data, NPOCStrategy, cash=100000)
# bt.run()
stats= bt.optimize(maximize="Equity Final [$]", nPOC_period=range(10, 50, 10))
print(stats)

# Evaluate the backtest results
bt.plot()
