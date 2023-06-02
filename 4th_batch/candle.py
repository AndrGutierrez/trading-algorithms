from backtesting import Backtest, Strategy
import talib
import pandas as pd
class SMAStrategy(Strategy):
    sma_period_short = 5
    sma_period_long = 20 
    def init(self):
        # Definimos los indicadores - SMA
        self.sma_short = self.I(talib.SMA, self.data.Volume, self.sma_period_short)
        self.sma_long = self.I(talib.SMA, self.data.Volume, self.sma_period_long)
    
    def next(self):
        # Si sma_short < sma_long, se realiza una compra
        if self.sma_short[-1] < self.sma_long[-1]:
            self.buy(sl = self.data.Close[-1] * 0.9, tp = self.data.Close[-1] * 1.5)

if __name__=='__main__':
    data = pd.read_csv('./data/uniswap/1h-2022-06-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]
    bt= Backtest(data, SMAStrategy, cash=100000)
    stats = bt.optimize(maximize='Equity Final [$]', 
                        sma_period_short=range(2, 10), 
                        sma_period_long=range(20, 40, 5))
    print(stats)
    bt.plot()