from backtesting import Strategy, Backtest
from backtesting.test import GOOG
import pandas as pd

class VolumeStrategy(Strategy):
    
    def init(self):
        self.volume_threshold = 0.5
    
    def next(self):
        volume_today = self.data.Volume[-1]
        volume_yesterday = self.data.Volume[-2]
        
        # Compramos si el volumen de hoy es mayor que el volumen de ayer por encima del umbral
        if volume_today > (volume_yesterday * (1 + self.volume_threshold)):
            self.buy()
        
        # Vendemos si el volumen de hoy es menor que el volumen de ayer por debajo del umbral
        if volume_today < (volume_yesterday * (1 - self.volume_threshold)):
            self.sell()

# creamos una instancia del objeto backtesting
# data=GOOG
data= pd.read_csv('./data/ETH-USD-1d-2022-05-04T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]

bt = Backtest(data, VolumeStrategy, cash=100000)

# ejecutamos el backtesting y obtenemos los resultados
results = bt.run()

print(results)
bt.plot()
# imprimimos el resumen de los resultados
