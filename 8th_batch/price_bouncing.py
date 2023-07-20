import backtesting as bt
import talib
import pandas as pd

class RsiBounceStrategy(bt.Strategy):
    bounces = 0
    rsi_period = 14
    rsi_oversold = 30
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)

    def next(self):
        # Calculate RSI

        if self.rsi[-1] > self.rsi_oversold and self.rsi[-2] <= self.rsi_oversold:
            self.bounces+=1
            if self.bounces == 3:
                self.bounces = 0
                self.buy(tp=self.data.Close[-1] * 1.2, sl=self.data.Close[-1] * 0.95)
            # If RSI is above oversold level, enter a long position
            # if not self.position:
                # self.buy()
        # else:
            # self.sell()

# Create a backtest
data = pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
data.columns = [column.capitalize() for column in data.columns]
bt = bt.Backtest(
    data,  # Your OHLC data
    RsiBounceStrategy,  # Strategy to test
    cash=100000,  # Initial capital
    commission=0.001,  # Commission for trading
)

# Run the backtest
# result = bt.run()
result = bt.optimize(maximize="Equity Final [$]", rsi_period=range(10, 30, 1), rsi_oversold=range(25, 40, 5))
# bt.run()

# Print the performance metrics
print(result)
bt.plot()
