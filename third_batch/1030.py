from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

class MyStrategy(Strategy):
    
    n1 = 9  # hora inicial (9:00AM) en minutos
    n2 = 10  # hora final (10:30AM) en minutos
    long_trend = False
    short_trend = False
    
    def init(self):
        self.long_trend = self.data.Close[:self.n1].mean() > self.data.Close[:self.n2].mean()  # verifica si hay tendencia bajista
        self.short_trend = self.data.Close[:self.n1].mean() < self.data.Close[:self.n2].mean()  # verifica si hay tendencia alcista

    def next(self):
        hora = self.data.Datetime[-1][-8:-3]
        diez_30=f'{self.n2}:30'
        # Si es las 10:30AM
        if hora == diez_30:
            if self.short_trend:
                self.buy()
            elif self.long_trend:
                self.sell()
    
data=pd.read_csv('./data/BTC-USD-15m-2023-01-04T00:00.csv')
data.columns= [column.capitalize() for column in data.columns]
# data['Datetime']=pd.to_datetime(data['Datetime'])
backtest = Backtest(
    data,  # data definida previamente
    MyStrategy,
    commission=.002,
    cash=100000,
    exclusive_orders=True
)

backtest.optimize(maximize='Equity Final [$]', n2=range(6, 15, 1))
backtest.plot()
print(backtest.report())