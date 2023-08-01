import backtesting
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd

class WickTestStrategy(Strategy):
    def init(self):
        self.reversal_candle = False

    def next(self):
        if len(self.data.Close) >= 3:
            if self.data.Close[-2] < self.data.Close[-3] and self.data.Close[-1] > self.data.Close[-2]:
                self.reversal_candle = True

            if self.reversal_candle and self.data.Close[-1] > self.data.Open[-1]:
                entry_price = self.data.High[-1]  # Entry at the high of the bullish candle (wick)
                self.buy(sl=entry_price * 0.95, tp=entry_price * 1.5)  # 1:2 risk-reward ratio

                # Reset the reversal_candle flag to avoid multiple entries
                self.reversal_candle = False

if __name__ == "__main__":
    data=pd.read_csv("./data/ethereum/4h-2021-07-01T00:00.csv")
    data= data.dropna()
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(data, WickTestStrategy, cash=100000, commission=0.002)
    stats=bt.run()
    print(stats)
    bt.plot()
