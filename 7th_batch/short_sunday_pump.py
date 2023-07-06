from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from datetime import datetime
import talib

class SundayPump(Strategy):
    def init(self):
        self.sma20 = self.I(talib.SMA, self.data.Close, 20)
        self.sma5 = self.I(talib.SMA, self.data.Close, 20)
    def next(self):
        date= pd.Timestamp(self.data.Datetime[-1]).to_pydatetime().weekday()
        isSunday=date==6
        if isSunday:
            self.buy(size=5, sl=self.data.Close[-1]*0.95, tp=self.data.Close[-1]*1.5)
           

data = pd.read_csv('./data/bitcoin/15m-2023-01-01T00:00.csv')
# data = pd.read_csv('./data/ethereum/15m-2023-01-01T00:00.csv')
data.datetime = pd.to_datetime(data.datetime)
# print(data.datetime[0])
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, SundayPump, cash=100000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()
