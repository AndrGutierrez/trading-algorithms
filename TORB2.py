import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class OpeningRangeStrategy(Strategy):
    opening_range_minutes = 30
    breakout = True

    def init(self):
        self.high = self.I(lambda x: pd.Series(x).rolling(self.opening_range_minutes).max(), self.data.High)
        self.low = self.I(lambda x: pd.Series(x).rolling(self.opening_range_minutes).min(), self.data.Low)

    def next(self):
        if len(self.data) <= self.opening_range_minutes:
            return

        if self.breakout:
            # Breakout strategy
            if self.data.Close[-1] > self.high[-2]:
                self.buy()
            elif self.data.Close[-1] < self.low[-2]:
                self.sell()
        else:
            # Reversal strategy
            if self.data.Close[-1] < self.low[-2] and crossover(self.data.Close, self.high[-2]):
                self.buy()
            elif self.data.Close[-1] > self.high[-2] and crossover(self.high[-2], self.data.Close):
                self.sell()

if __name__=="__main__":

    data = pd.read_csv('./data/BTC-USD-1d-2015-04-17T00:00.csv', index_col=0, parse_dates=True)
    data.columns=[column.capitalize() for column in data.columns]

    bt = Backtest(data, OpeningRangeStrategy, cash=10000, commission=.002)

    # Run the backtest with breakout strategy
    # stats_breakout = bt.run()
    range_minutes = range(10, 61, 5)

# Optimize the strategy by finding the best opening_range_minutes value
    optimization_results = bt.optimize(opening_range_minutes=range_minutes, maximize='Sharpe Ratio')

    # Run the backtest with reversal strategy
    # bt.strategy.breakout = False
    # stats_reversal = bt.run()
    bt.plot()