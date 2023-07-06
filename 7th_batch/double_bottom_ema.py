import backtesting
import talib
import pandas as pd

# Define the trading strategy
class DoubleBottomStrategy(backtesting.Strategy):
    # Define the parameters
    params = {
        'ema_length1': 5,
        'ema_length2': 8,
        'stop_loss_ratio': 0.02,
        'take_profit_ratio': 0.04
    }

    def init(self):
        self.ema1 = self.I(talib.EMA, self.data.Close, timeperiod=self.params['ema_length1'])
        self.ema2 = self.I(talib.EMA, self.data.Close, timeperiod=self.params['ema_length2'])

    # Define the trading logic
    def next(self):
        three_day_lowest= min(self.data.Low[-3:])
        # if self.data.Close[-1] > self.ema1[-1] and self.data.Close[0] < self.ema1[0]:
        if self.data.Close[-1] > self.ema1[-1]:
            # EMA crossover condition
            if self.data.Close[-1] > three_day_lowest or self.data.Close[0] < three_day_lowest:
                # Breakout condition
                entry_price = self.data.Close[-1]
                stop_loss = entry_price*0.95 
                take_profit = entry_price*1.07
                self.buy(sl=stop_loss, tp=take_profit)

# Load the historical price data (replace 'data.csv' with your own data file)
if __name__ == "__main__":
    # data = pd.read_csv("./data/bitcoin/1d-2020-01-01T00:00.csv")
    data = pd.read_csv("./data/bitcoin/1h-2022-01-01T00:00.csv")
    data.columns = [column.capitalize() for column in data.columns]

    bt = backtesting.Backtest(data, DoubleBottomStrategy, cash=100000, commission=0.001)
    results = bt.run()
    bt.plot()
    print(results)

    # Print the backtest results
    # print(results)
