import backtesting
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

class TripleRSIStrategy(Strategy):
    treshold1=30
    treshold2=50
    rsi_treshold = 50
    rsi_period=5
    def init(self):
        # Calculate the 5-day RSI
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        # Calculate the 200-day moving average
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

    def next(self):
        # Entry conditions
        if (
            self.rsi[-1] < self.treshold1 and
            self.rsi[-1] < self.rsi[-2] and
            self.rsi[-2] < self.rsi[-3] and
            self.rsi[-3] < self.treshold2 and
            self.data.Close[-1] > self.sma200[-1]
        ):
            self.buy()
            # self.buy()

        # Exit conditions
        if crossover(self.rsi, self.rsi_treshold):
            # self.sell(size=2)
            # self.sell()
            self.sell(size=3)

if __name__ == "__main__":
    data= pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(data, TripleRSIStrategy, cash=100000, commission=0.002)
    # results = bt.run()
    results = bt.optimize(maximize="Equity Final [$]", treshold2=range(40, 80, 5))
    print(results)
    bt.plot()
