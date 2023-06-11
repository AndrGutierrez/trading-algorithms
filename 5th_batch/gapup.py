from backtesting import Backtest, Strategy
import pandas as pd

class GapStrategy(Strategy):
    tp=1.2
    def init(self):
        pass
        # self.buy_signal = False
        # self.sell_signal = False
    def next(self):
        if self.data.Open[-1] > self.data.Close[-2] *1.0003:
            self.buy(tp=self.data.Open[-1]*self.tp, sl=self.data.Open[-1]*0.8)
data = pd.read_csv('./data/bitcoin/15m-2023-01-01T00:00.csv')
# fifteen_min_data = pd.read_csv('fifteen_minute_data.csv', parse_dates=True, index_col='DateTime')

data.columns=[column.capitalize() for column in data.columns]
bt=Backtest(data, GapStrategy, cash=100_000, commission=.002)
stats=bt.optimize(
    maximize='Equity Final [$]',
    tp=(1.10, 1.2, 1.3),

)
# stats=bt.run()
bt.plot()
