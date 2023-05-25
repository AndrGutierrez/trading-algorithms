import backtesting
from backtesting.lib import crossover
import talib
from backtesting.test import GOOG
import pandas as pd

class SMAStrategy(backtesting.Strategy):
    periodo1=10
    periodo2=50
    def init(self):
        self.sma1 = self.I(talib.SMA, self.data.Close, timeperiod=self.periodo1)
        self.sma2 = self.I(talib.SMA, self.data.Close, timeperiod=self.periodo2)
        self.volume = self.data.Volume
    
    def next(self):
        if crossover(self.sma1, self.sma2) or (self.volume[-1] > self.volume[-2]* 1.1):
            self.buy()
        
        elif crossover(self.sma2, self.sma1):
            self.sell()

# data= GOOG
data= pd.read_csv('./data/BTC-USD-1d-2022-06-04T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]
bt= backtesting.Backtest(data, SMAStrategy, commission=0.002, cash=100000)
results = bt.optimize(
    maximize='Equity Final [$]',
    periodo1= range(5,15, 1),
    periodo2= range(30,70, 5),
)
print(results)
bt.plot()