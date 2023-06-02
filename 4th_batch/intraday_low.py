import backtesting
import talib
import pandas as pd

class SMA4Strategy(backtesting.Strategy):

    period=4
    def init(self):
        self.sma4 = self.I(talib.SMA, self.data.Close, timeperiod=self.period)

    def next(self):
        time = pd.Timestamp(self.data.Datetime[-1]).to_pydatetime().hour
        if time == 14:
            if self.data.Close[-1] > self.sma4[-1]:
                if self.data.Close[-1] <= min(self.data.Close[-7:]):
                        self.buy()
            elif self.data.Close[-1] < self.sma4[-1]:
                if self.data.Close[-1] >= max(self.data.Close[-7:]):
                    self.sell()

data= pd.read_csv('./data/uniswap/1h-2022-06-01T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]
bt = backtesting.Backtest(data, SMA4Strategy, commission=0.002, cash=100000)
output = bt.optimize(maximize='Equity Final [$]', period=range(2, 20))
print(output)
bt.plot()