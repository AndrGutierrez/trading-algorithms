import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd

class BollingerBandRibbonStrategy(Strategy):
    timeperiod = 20
    def init(self):
        # self.upper, self.middle, self.lower = talib.BBANDS(self.data.Close, timeperiod=self.timeperiod, nbdevup=0.618, nbdevdn=0.618)
        self.upper, self.middle, self.lower = talib.BBANDS(self.data.Close, timeperiod=self.timeperiod, nbdevup=0.618, nbdevdn=0.618)

    def next(self):
        if crossover(self.upper, self.data.Close) and self.data.Close[-1] > self.upper[-1]:
            self.buy(size=1, sl=self.lower[-1], tp=self.upper[-1])
        elif crossover(self.data.Close, self.middle):
            self.sell()

        # Check for sell signal
        # elif self.data.Close[-1] < self.upper[-1] or crossover(self.data.Close, self.middle):
        #     self.sell()

if __name__ == "__main__":
    # data=pd.read_csv("./data/bitcoin/15m-2023-01-01T00:00.csv")
    # data=pd.read_csv("./data/ethereum/15m-2023-01-01T00:00.csv")
    data=pd.read_csv("./data/ethereum/5m-2023-04-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(data, BollingerBandRibbonStrategy, cash=100000)
    # bt.run()
    stats = bt.optimize(maximize="Equity Final [$]", timeperiod=range(5, 45, 5))
    # bt.run()
    bt.plot()
