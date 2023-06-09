from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd

class SMACross(Strategy):
    period_long=20
    def init(self):
        volume = self.data.Volume
        self.close_df = pd.DataFrame(self.data.Close, columns=['Close'])
        self.sma20 = self.I(talib.SMA, volume, timeperiod=self.period_long)

    def next(self):
        lows=self.close_df.Close.nsmallest(1)

        # if crossover(self.data.Close, self.sma20):
        if self.data.Close[-1] > self.sma20[-1]:
            # print(lows.iloc[0])
            self.buy(sl=lows.iloc[0], tp=2*self.data.Close[-1])

data=pd.read_csv("./data/bitcoin/15m-2023-01-01T00:00.csv")
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, SMACross, cash=100000, commission=.002)
stats = bt.optimize(maximize='Equity Final [$]',  period_long=range(20, 100, 5))
bt.plot()
