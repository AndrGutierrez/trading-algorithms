from backtesting.test import GOOG

import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Importa tus datos aquí (un DataFrame de Pandas con las columnas 'Open', 'High', 'Low', 'Close', 'Volume')
# data = ...

class MovingAverageStrategy(Strategy):
    n = 50  # Media móvil de 50 días

    def init(self):
        # Calcula la media móvil simple (SMA) de 50 días
        self.sma = self.I(talib.SMA, self.data.Close, self.n)

    def next(self):
        # Compra si el precio de cierre cruza por encima de la SMA de 50 días
        if crossover(self.data.Close[-1], self.sma):
            self.buy()

        # Vende si el precio de cierre cruza por debajo de la SMA de 50 días
        elif crossover(self.sma, self.data.Close[-1]):
            self.sell()
data= pd.read_csv("data/ETH-USD-1d-2022-05-04T00:00.csv")
data.columns= [column.capitalize() for column in data.columns]
bt = Backtest(data, MovingAverageStrategy, cash=100000, commission=.002)
stats = bt.optimize(
    maximize='Equity Final [$]',
    n=[20, 30, 50]
)

print(stats)

# Gráfica de la estrategia
bt.plot()

# data= pd.read_csv("./data/BTC-USD-1d-2022-05-04T00:00.csv")