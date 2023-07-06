import backtesting
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class MovingAverageStrategy(Strategy):
    timeperiod=7
    smaperiod=200
    def init(self):
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=self.smaperiod)
        self.lowest_low = self.I(talib.MIN, self.data.Low, timeperiod=7)
        self.highest_high = self.I(talib.MAX, self.data.High, timeperiod=7)
    
    def next(self):
        # print(self.data.Close[-1], self.highest_high[-1])
        if self.data.Close[-1] > self.sma200[-1] or self.data.Close[-1] <= self.lowest_low[-1]:
            self.buy(size=10, sl=self.data.Close[-1]*0.95, tp=self.data.Close[-1]*1.20)
            # self.buy()
            # self.buy(sl=self.data.Close[-1]*0.95)
            # self.buy(size=1,tp=self.data.Close[-1]*1.1)
            # self.buy()
        
        elif self.data.Close[-1] < self.highest_high[-1]:
        # elif crossover(self.highest_high, self.data.Close):
            # self.position.close()
            self.sell()
            # pass

# Assuming you have a CSV file named 'price_data.csv' with columns: 'Date', 'Open', 'High', 'Low', 'Close'
# data = pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
data = pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, MovingAverageStrategy, cash=100000, commission=.002)
# results = bt.run()
results = bt.optimize(maximize='Equity Final [$]', timeperiod=range(5,10), smaperiod=range(100, 300, 20))
print(results)
bt.plot()

