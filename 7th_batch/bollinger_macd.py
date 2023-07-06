import backtesting
import talib
import pandas as pd
from backtesting.lib import crossover

class BBANDS_MACD_Strategy(backtesting.Strategy):
    timeperiod=20
    def init(self):
        self.bbolinger, _, _ = self.I(talib.BBANDS, self.data.Close, timeperiod=self.timeperiod, nbdevup=2, nbdevdn=2)
        self.macd, self.signal, _ = self.I(talib.MACD, self.data.Close)

    def next(self):
        if crossover(self.data.Close, self.bbolinger) and crossover(self.macd, self.signal):
            self.buy(size=1, sl=self.data.Close*0.98, tp=self.data.Close*1.05)  # Set stop loss 10 pips away from entry
        elif crossover(self.bbolinger, self.data.Close) and crossover(self.signal, self.macd):
            self.sell()

# Prepare the data
# data = backtesting.get_data("AAPL", start_date="2022-01-01", end_date="2022-12-31")
data=pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
# data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
data.columns=[column.capitalize() for column in data.columns]

# Initialize and run the backtest
bt = backtesting.Backtest(data, BBANDS_MACD_Strategy, cash=100000, commission=0.002)
stats=bt.optimize(maximize="Equity Final [$]", timeperiod=range(20, 60, 5))
bt.plot()

print(stats)
# Analyze the results
# print(bt.get_profit_and_loss())
