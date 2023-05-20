from backtesting import Backtest, Strategy
import talib
import pandas as pd
from backtesting.test import GOOG

class PullBackStrategy(Strategy):

    stop_loss = 0
    n1 = 20

    def init(self):
        price = self.data.Close
        self.sma = self.I(talib.SMA, price, self.n1)

    def next(self):
        price = self.data.Close[-1]
        low_price_prev_day = self.data.Low[-2]  # Precio más bajo del día anterior

        if price > self.sma[-1]:  # Si el precio está por encima de la SMA de 20 días
            self.stop_loss = low_price_prev_day  # Establecer stop loss al precio más bajo del día anterior


            # Comprar si el precio es 1.5 veces el stop loss
            if price <= 2.5 * self.stop_loss:
                self.buy()

# Cargar datos OHLCV en un DataFrame
data = pd.read_csv('./data/ETH-USD-1d-2022-05-04T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]
# data=GOOG

# Crear e iniciar el backtest
bt = Backtest(data, PullBackStrategy, cash=100000, commission=.002)
output = bt.optimize(maximize='Equity Final [$]', n1=range(5, 40, 1))
print(output)
bt.plot()