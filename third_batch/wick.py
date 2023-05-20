
from backtesting import Backtest, Strategy
from backtesting.lib import SignalStrategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import pandas as pd

class HighLowStrategy(SignalStrategy, Strategy):
    margen=1
    def init(self):
        self.buy_price = 0  # Precio de compra inicial
        self.profit_potential = 0  # Potencial de ganancias inicial
        self.sell_price = 0  # Precio de venta inical
        self.high_previous = 0  # High del día anterior
        
    def next(self):
        marg= (self.margen /100)+1
        # Compra
        if self.data.Close[-1] - self.data.Low[-1] * marg > 0:
            self.buy_price = self.data.Close[-1]  # Precio de compra
            self.buy()
            
        # Venta si se han generado ganancias
        if self.data.High[-1] > self.data.High[-2] * marg :
            self.sell()


data= pd.read_csv('./data/ETH-USD-1d-2022-05-04T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, HighLowStrategy, cash=1000000, commission=.002)
output = bt.optimize(maximize='Equity Final [$]', margen=range(1,100, 1))
bt.plot()