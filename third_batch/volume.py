from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import pandas as pd

class BuyOnVolumeDropSellOnVolumeSurge(Strategy):
    def init(self):
        # Definimos una variable para guardar el precio de compra
        self.buy_price = None
    
    def next(self):
        # Si el volumen ha bajado un 10% o más respecto al día anterior y no tenemos una posición abierta, compramos
        if self.data.Volume[-1] < 0.9 * self.data.Volume[-2] and not self.position:
            self.buy()
            self.buy_price = self.data.Close[-1]
            
        # Si el precio sube un 2% o más respecto del precio de compra, vendemos
        elif self.position and crossover(self.data.Close, self.buy_price * 1.02):
            self.sell()
    
data= pd.read_csv('./data/UNI-USD-1d-2022-05-04T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
bt = Backtest(data, BuyOnVolumeDropSellOnVolumeSurge, cash=100000)
bt.run()
bt.plot()
