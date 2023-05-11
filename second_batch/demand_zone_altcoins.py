import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

def capitalize_columns(data):
    return [column.capitalize() for column in data.columns]
class RSI_Zone_Strategy(Strategy):
    rsi_period = 14
    rsi_low = 30
    rsi_high = 70

    def init(self):
        btc_data = pd.read_csv('./data/altcoins_btc/MATIC-USD-1d-2022-05-04T00:00.csv', index_col=0, parse_dates=True)
        btc_data.columns= capitalize_columns(btc_data)
        btc_close= btc_data['Close']
        self.rsi = self.I(talib.RSI, btc_close, self.rsi_period)

    def next(self):
        if self.rsi[-1] < self.rsi_low:
            # Comprar cuando el RSI está en zona de demanda
            self.buy()
        elif self.rsi[-1] > self.rsi_high and self.position:
            # Vender cuando el RSI sale de zona de demanda
            self.sell()

# Carga de datos históricos
data = pd.read_csv('./data/altcoins_btc/MATIC-USD-1d-2022-05-04T00:00.csv', index_col=0, parse_dates=True)
data.columns= capitalize_columns(data)
# Inicializar el backtesting
bt = Backtest(data, RSI_Zone_Strategy, cash=100000, commission=.002)


# Optimizar los parámetros del algoritmo de trading
params = bt.optimize(rsi_period=range(10, 30, 1),
                     rsi_low=range(10, 40, 1),
                     rsi_high=range(50, 80, 1),
                    #  maximize='Sharpe Ratio',
                     maximize='Equity Final [$]',
                     constraint=lambda param: param.rsi_low < param.rsi_high
                     )
# Imprimir los parámetros óptimos
bt.plot()