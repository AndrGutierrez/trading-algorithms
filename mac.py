import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class MovingAverageCrossover(Strategy):
    short_ma = 20
    long_ma = 50

    def init(self):
        # Compute moving averages
        self.short_ma = self.I(pd.DataFrame(self.data.Close.rolling), self.short_ma).mean()
        self.long_ma = self.I(pd.DataFrame(self.data.Close.rolling), self.long_ma).mean()

    def next(self):
        # Execute orders if the short MA crosses over/under the long MA
        if crossover(self.short_ma, self.long_ma):
            self.position.close()
            self.buy()
        elif crossover(self.long_ma, self.short_ma):
            self.position.close()
            self.sell()

if __name__ == "__main__":
    # Load your data (CSV with columns: "Open", "High", "Low", "Close", "Volume")
    data = pd.read_csv("./data/ETH-USD-1d-2022-08-12T00:00.csv", index_col=0, parse_dates=True)
    data.columns=[column.capitalize() for column in data.columns]

    bt = Backtest(data, MovingAverageCrossover, cash=10000, commission=0.002)
    stats = bt.run()

    print(stats)
    bt.plot()