import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

class RSI_Zone_Strategy(Strategy):
    rsi_period = 14
    rsi_low = 30
    rsi_high = 70

    def init(self):
        close = self.data.Close
        self.rsi = self.I(talib.RSI, close, self.rsi_period)

    def next(self):
        print(self.position)
        if self.rsi[-1] < self.rsi_low:
            # Comprar cuando el RSI está en zona de demanda
            self.buy()
        elif self.rsi[-1] > self.rsi_high and self.position:
            # Vender cuando el RSI sale de zona de demanda
            self.sell()

# Carga de datos históricos
# data = pd.read_csv('./data/UNI-USD-1d-2022-05-04T00:00.csv', index_col=0, parse_dates=True)
data=GOOG

data.columns=[column.capitalize() for column in data.columns]
# Inicializar el backtesting
bt = Backtest(data, RSI_Zone_Strategy, cash=100000, commission=.002)

# Ejecutar el backtesting y obtener estadísticas
# stats = bt.run()
# print(stats)

# Optimizar los parámetros del algoritmo de trading
# params = bt.run()
params = bt.optimize(rsi_period=range(10, 20, 2),
                     rsi_low=range(20, 40, 5),
                     rsi_high=range(60, 80, 5),
                     maximize='Sharpe Ratio',
                    #  constraint=lambda param: param.rsi_low < param.rsi_high
                     )
# Imprimir los parámetros óptimos
print(params)
bt.plot()