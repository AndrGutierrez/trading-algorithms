from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


class MiEstrategia(Strategy):
    def init(self):
        # Define el close del día anterior
        self.ultimo_cierre = self.data.Close[-1]

    def next(self):
        # Si el Low es menor que el Close actual, compra
        if self.data.Low[-1] - self.data.Close[-1] > 0:
            self.buy()
        # Si el High es mayor que el Close del día anterior, compra
        elif self.data.High[-1] > self.ultimo_cierre:
            self.buy()
        # Actualiza el último cierre
        self.ultimo_cierre = self.data.Close[-1]


bt = Backtest(GOOG, MiEstrategia)
stats = bt.run()
bt.plot()
