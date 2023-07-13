from backtesting import Backtest, Strategy
import pandas as pd

class Triple(Strategy):
    tp=10
    sl=5
    def init(self):
        pass
    def next(self):
        if len(self.data.Close) < 3: return
        if self.data.Close[-1] > self.data.Close[-2] > self.data.Close[-3]:
            self.buy(tp=self.data.Close[-1] * (1 + self.tp/1000), sl=self.data.Close[-1] * (1-self.sl/1000))

if __name__ == "__main__":
    data=pd.read_csv("./data/ETH-USD-3m-2023-07-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt=Backtest(data, Triple, cash=100000)
    bt.optimize(maximize='Equity Final [$]', tp=range(10, 30), sl=range(10, 30))
    bt.plot()
