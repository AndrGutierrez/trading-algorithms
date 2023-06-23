from backtesting import Backtest, Strategy
import pandas as pd
from backtesting.lib import crossover

class SmaScalper(Strategy):
    timeframe = 475
    def init(self):
            self.smma = self.I(calculate_smma, self.data.Close, self.timeframe)

    def next(self):
        if crossover(self.data.Close, self.smma):
        # if crossover(self.smma, self.data.Close):
            # stop_loss= self.data.High[-2] if self.data.High[-2] < self.data.High[-1] else 0
            stop_loss= self.data.Close[-2]*0.97 if self.data.Close[-2] < self.data.Close[-1] else 0
            self.buy(sl=stop_loss, tp= self.data.Close[-1] * 1.05)
        # else:
        #     self.sell()


def calculate_smma(data, period):
    smma = []
    prev_smma = sum(data[:period]) / period  # Initial SMMA value is the simple average of the first 'period' data points
    smma.append(prev_smma)

    for i in range(1, len(data)):
        current_smma = (prev_smma * (period - 1) + data[i]) / period  # SMMA calculation formula
        smma.append(current_smma)
        prev_smma = current_smma

    return smma

if __name__ == '__main__':
    # data= pd.read_csv("./data/bitcoin/4h-2020-01-01T00:00.csv")
    data= pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    # data= pd.read_csv("./data/ethereum/4h-2020-01-01T00:00.csv")
    # data= pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    data=data.dropna()
    data.columns = [column.capitalize() for column in data.columns]

    bt= Backtest(data, SmaScalper, cash=100000, commission=.002)
    bt.optimize(maximize='Equity Final [$]', timeframe=range(400, 450, 10))
    bt.plot()
