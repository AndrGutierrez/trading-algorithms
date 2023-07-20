import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd

class BollingerBandRibbonStrategy(Strategy):
    timeperiod = 20
    deviation = 618
    def init(self):
        dev = self.deviation / 1000
        # self.upper, self.middle, self.lower = talib.BBANDS(self.data.Close, timeperiod=self.timeperiod, nbdevup=0.618, nbdevdn=0.618)
        self.upper, self.middle, self.lower = talib.BBANDS(self.data.Close, timeperiod=self.timeperiod, nbdevup=dev, nbdevdn=dev)

    def next(self):
        if self.upper[-1] > self.data.Close[-1] and self.data.Close[-1] > self.upper[-1]:
            self.buy(sl=self.lower[-1], tp=self.upper[-1])
        elif crossover(self.data.Close, self.upper):
            self.sell()


if __name__ == "__main__":
    data=pd.read_csv("./data/bitcoin/15m-2023-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(data, BollingerBandRibbonStrategy, cash=100000)
    stats = bt.optimize(maximize="Equity Final [$]", timeperiod=range(5, 45, 5), deviation=range(500, 2000, 100))
    # stats=bt.run()
    print(stats)
    bt.plot()
