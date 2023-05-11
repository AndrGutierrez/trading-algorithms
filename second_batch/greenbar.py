
import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

class ConsolidacionRevalorizacionEstrategia(Strategy):
    rsi_period = 14
    rsi_range = (40, 60)
    take_profit_pct = 0.05

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)

    def next(self):
        rsi_actual = self.rsi[-1]
        precio_actual = self.data.Close[-1]

        if self.position.is_long:
            if (precio_actual / self.data.Open) - 1 >= self.take_profit_pct:
                self.position.close()

        if not self.position and self.rsi_range[0] <= rsi_actual <= self.rsi_range[1]:
            self.buy()

if __name__ == '__main__':
    # Cargar datos históricos de precios
    # data = pd.read_csv('./data/bitcoin/5m-2023-03-27T00:00.csv', index_col=0, parse_dates=True)
    data = pd.read_csv('./data/ETH-USD-1d-2022-05-04T00:00.csv', index_col=0, parse_dates=True)
    # data = pd.read_csv('./data/uniswap/1h-2023-03-27T00:00.csv', index_col=0, parse_dates=True)
    data.columns=[column.capitalize() for column in data.columns]

    # Inicializar el backtest
    bt = Backtest(data, ConsolidacionRevalorizacionEstrategia, cash=100000, commission=.002)

    # Ejecutar el backtest y mostrar los resultados
    stats = bt.run()
    print(stats)
    bt.plot()