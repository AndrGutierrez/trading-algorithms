from backtesting.lib import crossover
import pandas as pd
from backtesting import Backtest, Strategy
import talib

class PSARStrategy(Strategy):
    sma_period1=8
    sma_period2=21
    atr_period=14
    def init(self):
        self.sma1 = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period1)
        self.sma2 = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period2)
        self.psar = self.I(talib.SAR, self.data.High, self.data.Low, 0.2, 0.2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)

    def next(self):
        sma_trending_upwards=crossover(self.sma1, self.sma2)
        if self.data.Close[-1] > self.sma1[-1] or self.sma1[-1] > self.sma2[-1] or sma_trending_upwards or self.psar[-1] > self.data.Close[-1]:
            # if self.data.Close[-1] > self.sma1[-1] and self.data.Close[-2] < self.sma1[-2]:
            # self.buy(sl=self.data.Close[-1] * 0.97, tp=self.data.Close[-1] * 1.3)
            self.buy(tp=self.data.Close[-1] * 1.4)
        else:
            # if self.data.Close[-1] < self.sma1[-1] and self.data.Close[-2] > self.sma1[-2]:
                # self.sell(size=1)
                self.sell()

if __name__=="__main__":
    # data=pd.read_csv("./data/bitcoin/4h-2021-07-01T00:00.csv")
    # data=pd.read_csv("./data/ethereum/4h-2021-07-01T00:00.csv")
    # data=pd.read_csv("./data/bitcoin/15m-2023-01-01T00:00.csv")
    data=pd.read_csv("./data/ethereum/15m-2023-01-01T00:00.csv")
    data = data.dropna()
    data.columns = [column.capitalize() for column in data.columns]
    bt = Backtest(data, PSARStrategy, cash=100000, commission=.002)
    stats=bt.run()
    # stats= bt.optimize(maximize='Equity Final [$]', sma_period1=range(5, 15), sma_period2=range(20, 50, 5))
    bt.plot()
