import backtesting
import talib
import pandas as pd
from backtesting.lib import crossover 

class SMACrossoverStrategy(backtesting.Strategy):
    n1=5
    n2=20
    def init(self):
        self.sma5 = self.I(talib.SMA, self.data.Close, timeperiod=self.n1)
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=self.n2)
        
    def next(self):
        if crossover(self.sma5, self.sma20) and self.data.Volume[-1] > 2*self.data.Volume[-2]:
            # self.buy(tp=self.data.Close[-1]*1.1, sl=self.data.Close[-1]*0.8)
            self.buy()
        elif crossover(self.sma20, self.sma5):
            self.buy(tp=self.data.Close[-1]*1.1, sl=self.data.Close[-1]*0.8)
            # self.sell()

if __name__== "__main__":
    # data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    # data = pd.read_csv("./data/bitcoin/1d-2020-01-01T00:00.csv")
    # data = pd.read_csv("./data/bitcoin/15m-2023-01-01T00:00.csv")

    data = pd.read_csv("./data/ethereum/15m-2023-01-01T00:00.csv")
    # data = pd.read_csv("./data/ethereum/1d-2020-01-01T00:00.csv")
    data.columns = [column.capitalize() for column in data.columns]
    bt = backtesting.Backtest(data, SMACrossoverStrategy, cash=100000, commission=.002)
    bt.optimize(maximize="Equity Final [$]", n1=range(5, 20, 1), n2=range(20, 60, 5))
    bt.plot()
