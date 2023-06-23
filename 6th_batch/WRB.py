from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd
import statistics

class MyStrategy(Strategy):
    average_timeperiod = 10
    n1=5
    n2=20
    def init(self):
        self.sma5 = self.I(talib.SMA, self.data.Close, timeperiod=self.n1)
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=self.n2)
        self.stop_loss_percent = 0.9
        self.bearish_trend = False
        
    def next(self):
    
        sizes=[]
        def calculate_size():
            last_ten_close= self.data.Close[-self.average_timeperiod:]
            last_ten_open= self.data.Open[-self.average_timeperiod:]
            for i in range(self.average_timeperiod):
                    sizes.append(abs(last_ten_close[i] - last_ten_open[i]))
        calculate_size()

        # print(sizes)
        average_size=statistics.mean(sizes)
        current_candle_size = abs(self.data.Close[-1] - self.data.Open[-1])
        # average_candle_size = self.average_candle_size[-1]
        
        if current_candle_size >= 2 * average_size:
            self.bearish_trend = self.data.Close[-1] > self.data.Open[-1]
        
        if self.bearish_trend and self.sma5[-1] > self.sma20[-1] and self.sma5[-2] < self.sma20[-2]:
            # self.buy(sl=self.data.Close[-1] * self.stop_loss_percent)
            self.buy()
        else:
                self.sell(size=1)

if __name__=="__main__":
    # data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data = pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    data = data.dropna()
    data.columns = [column.capitalize() for column in data.columns]
    bt=Backtest(data, MyStrategy, cash=100_000, commission=.002)
    stats = bt.optimize(maximize='Equity Final [$]', n1=range(5, 15), n2=range(15, 50, 5))
    bt.plot()
