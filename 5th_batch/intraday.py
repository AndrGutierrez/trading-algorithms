from backtesting import Backtest, Strategy
import pandas as pd

class MeanReversionStrategy(Strategy):
    n1 = 240
    tp=25

    def init(self):
        close_prices = self.data.Close
        self.lowest_n1 = self.I(lambda x: pd.DataFrame(x).rolling(self.n1).min(), close_prices)

    def next(self):
        low_value = self.lowest_n1[-1]
        if self.data.Close[-1] <= low_value * 1.1:
            self.buy(sl=self.data.Close[-1] * 0.8, tp=self.data.Close[-1]*((self.tp/100)+1))

if __name__ == '__main__':
    data = pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')  # Load your data into a DataFrame
    data.columns=[column.capitalize() for column in data.columns]
    bt = Backtest(data, MeanReversionStrategy, cash=100000, commission=.002)
    stats = bt.optimize(maximize='Equity Final [$]', n1=range(24, 480, 10), tp=range(5, 35, 5))
    bt.plot()
