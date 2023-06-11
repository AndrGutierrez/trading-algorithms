import pandas as pd
from backtesting import Backtest, Strategy
from talib import SMA


class MyStrategy(Strategy):
    take_profit=3
    n2=20
    n1=5
    def init(self):
        # Precompute the two moving averages
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
        self.sma1= self.I(SMA, self.data.Close, self.n1)
        pass


    def next(self):
        # If sma5 < sma20, enter (or stay in) the long position
        if self.sma1[-1]>self.sma2[-1]:
            tp = self.data.Close[-1] * (1+(self.take_profit/100))
            sl = self.data.Close[-1] * 0.9
            # If we're in the long position and price closes above TP, or below SL, exit
            self.buy(sl=sl, tp=tp)

    def identify_demand_zone(self):
        # Set the window size for calculating the demand zone
        window = 20

        # Get the minimum price in the window
        low = self.data.Low[-window:].min()

        # Get the maximum price in the window
        high = self.data.High[-window:].max()

        # Set the threshold for a significant price drop and recovery (e.g., 3%)
        threshold = 0.03

        # Check if the price dropped significantly in the window
        if (high - low) / high >= threshold:
            # Check if the price has recovered to above the demand zone
            if self.data.Close[-1] >= high:
                return True 

        # If no demand zone was identified, return the latest low and high prices
        return False 


def crossover(a, b):
    """
    Returns True if a crosses over b, else False
    """
    return a[-2] < b[-2] and a[-1] > b[-1]


if __name__ == '__main__':
    # Read data
    data = pd.read_csv('./data/ethereum/1h-2022-01-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]

    bt = Backtest(data, MyStrategy, cash=100_000, commission=.002)
    output = bt.optimize(maximize='Equity Final [$]', take_profit=range(1, 4))


    print(output)
    bt.plot()
