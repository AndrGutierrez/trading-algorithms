import numpy as np
import backtesting
import talib
import pandas as pd
from backtesting.lib import crossover

class BBANDS_EMA_Strategy(backtesting.Strategy):
    timeperiod=20
    ema_period=20
    def init(self):
        self.upper_band, self.middle_band, self.lower_band = self.I(talib.BBANDS, self.data.Close, timeperiod=self.timeperiod, nbdevup=2, nbdevdn=2)
        self.ema = self.I(talib.EMA, self.data.Close, timeperiod=self.timeperiod)

    def next(self):
        if crossover(self.data.Close, self.upper_band) or crossover(self.ema, self.data.Close):
            # self.buy()
            self.buy(tp=self.data.Close*1.1, sl=self.data.Close*0.95)
        elif crossover(self.data.Close, self.ema):
            self.sell(size=2)
            pass
        #     self.sell(size=1)

if __name__ == '__main__':
    # Prepare the data
    # data=pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
    data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]

    # Initialize and run the backtest
    bt = backtesting.Backtest(data, BBANDS_EMA_Strategy, cash=100000, commission=0.002)
    stats=bt.optimize(maximize="Equity Final [$]", timeperiod=range(20, 60, 5))
    # stats=bt.run()
    print(stats)
    bt.plot()

    # Analyze the results
    # print(bt.get_profit_and_loss())
