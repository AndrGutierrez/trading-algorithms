from backtesting import Backtest, Strategy
import pandas as pd

class GapStrategy(Strategy):
    tp = 1.03
    sl = 0.997
    margin=1.0003
    def init(self):
        pass
        # self.buy_signal = False
        # self.sell_signal = False
    def next(self):
        if self.data.Open[-1] > self.data.Close[-2] *self.margin:
            self.buy(tp=self.data.Close[-1]*self.tp, sl=self.data.Close[-1]*self.sl)

# fifteen_min_data = pd.read_csv('fifteen_minute_data.csv', parse_dates=True, index_col='DateTime')
data = pd.read_csv('./data/bitcoin/5m-2023-04-01T00:00.csv')

data.columns=[column.capitalize() for column in data.columns]
bt=Backtest(data, GapStrategy, cash=100_000)
stats=bt.optimize(
    maximize='Equity Final [$]',
    tp=(1.01, 1.02, 1.03, 1.04, 1.05),
    sl=(0.99, 0.98, 0.97, 0.96, 0.95),
)
# bt.run()
bt.plot()
