import backtesting
import talib
import pandas as pd
from backtesting.lib import crossover

# Define the strategy
class MovingAverageCrossover(backtesting.Strategy):
    buy_trigger_bar = 999999
    sell_trigger_bar = 0
    short_period=9
    long_period=30
    def init(self):
        self.ema9 = self.I(talib.EMA, self.data.Close, timeperiod=self.short_period)
        self.ema30 = self.I(talib.EMA, self.data.Close, timeperiod=self.long_period)
        self.wma9 = self.I(talib.WMA, self.data.Close, timeperiod=self.short_period)
        self.wma30 = self.I(talib.WMA, self.data.Close, timeperiod=self.long_period)
        self.trigger_bar = None

    def next(self):
        if self.data.Close[-1] < self.ema30[-1]:
            self.buy_trigger_bar=self.data.Close[-1]
        if crossover(self.ema9, self.ema30):
        # if crossover(self.ema9, self.ema30) or self.data.Close[-1] > self.buy_trigger_bar:
            # Bullish crossover, generate a buy signal
            # self.buy(size=3)
            self.buy(size=3)
        if self.data.Close[-1] > self.ema30[-1]:
            self.sell_trigger_bar=self.data.Close[-1]
        # elif (self.ema9[-1] > self.wma30[-1] and self.ema9[-1] < self.wma30[-1]) or self.data.Close[-1] < self.sell_trigger_bar:
        elif self.ema9[-1] > self.wma30[-1]:
            # Bearish crossover, generate a sell signal
            # self.sell(size=3)
            self.sell(size=3)


# Prepare the data
if __name__ == '__main__':
    data = pd.read_csv("./data/ethereum/1d-2021-07-01T00:00.csv") 
    data.columns=[column.capitalize() for column in data.columns]

    # Run the backtest
    bt = backtesting.Backtest(data, MovingAverageCrossover, cash=100000, commission=0.002)
    # results = bt.run()
    results=bt.optimize(maximize="Equity Final [$]", short_period=range(5, 30, 5), long_period=range(30, 60, 5))

    # Analyze the results
    print(results)
    bt.plot()

