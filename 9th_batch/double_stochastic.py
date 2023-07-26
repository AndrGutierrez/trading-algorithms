import backtesting
import talib
from backtesting.lib import crossover, cross
import pandas as pd

# Define the trading strategy
class StochasticStrategy(backtesting.Strategy):
    period_long = 21
    period_short = 9
    def init(self):
        # Set parameters for Stochastic (21,9,9) and (9,3,3)
        self.long_k, self.long_d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, self.period_long, slowk_period=9, slowd_period=9)
        self.short_k, self.short_d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, self.period_short, slowk_period=3, slowd_period=3)
        # Set initial state
        self.long_entry = False

    def next(self):
        # Wait for stochastic (21,9,9) crossover to enter or wait for the current bar to close
        if crossover(self.long_k, self.long_d) and not self.long_entry:
            self.buy(tp=self.data.Close[-1] * 1.1, sl=self.data.Close[-1] * 0.9)
            self.long_entry = True
        elif self.long_entry: 
            # Check for additional entries using stochastic (9,3,3)
            if crossover(self.short_k, self.short_d):
                self.sell()

        # Exit if major stochastic (21,9,9) lines cross again
        # if crossover(self.long_k, self.long_d):
        # else:
        #     self.sell()
        #     self.long_entry = False
        if cross(self.long_k, self.long_d):
            # self.position.close()
            self.sell(size=1)
            self.long_entry = False

data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    # data = pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
data.columns=[column.capitalize() for column in data.columns]

# Create and run the backtest
bt = backtesting.Backtest(data, StochasticStrategy, cash=100000, commission=0.002)
stats = bt.run()
stats = bt.optimize(maximize='Equity Final [$]',
                    period_long=range(20, 50, 5),
                    period_short=range(5, 20, 2))

# Print the backtest results
print(stats)
bt.plot()
