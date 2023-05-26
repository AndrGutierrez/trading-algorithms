from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import talib
import pandas as pd


class MyStrategy(Strategy):
    timeperiod=14
    def init(self):
        self.macd, self.signal, self.hist = self.I(talib.MACD, self.data.Close)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=self.timeperiod)
        self.market_is_bullish= False
    def next(self):
        if self.macd[-1] > self.signal[-1] :
            market_is_bullish=True
        elif self.macd[-1] < self.signal[-1]:
            market_is_bullish=False
        # Si el último valor del ADX es mayor que 20 y no tenemos posiciones abiertas, abrimos una posición larga
        if self.adx[-1] > 20 :
            # self.buy(sl=self.data.Close[-1]*0.97) # ponemos un stop loss del 3%
            if market_is_bullish:
                self.buy() # ponemos un stop loss del 3%
            else:
                self.sell() # ponemos un stop loss del 3%

# data=GOOG
data = pd.read_csv('./data/ETH-USD-1d-2022-06-04T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]
bt = Backtest(data, MyStrategy, commission=.002, cash=100000)
stats = bt.optimize(maximize='Equity Final [$]', timeperiod=range(10, 30))
bt.plot()