import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

class DipReboundStrategy(Strategy):
    dip_threshold = -5
    rebound_threshold = 3

    def init(self):
        self.close_prices = self.I(lambda x: x, self.data.Close)

    def next(self):
        current_price = self.close_prices[-1]
        prev_price = self.close_prices[-2]

        price_change = ((current_price - prev_price) / prev_price) * 100

        if price_change <= self.dip_threshold:
            self.buy()
        elif self.position and price_change >= self.rebound_threshold:
            self.sell()

if __name__ == "__main__":
    data_csv= './data/ethereum/1h-2023-03-27T00:00.csv'
    # data_csv= './data/ETH-USD-1d-2022-04-17T00:00.csv'
    data = pd.read_csv(data_csv, index_col=0, parse_dates=True)
    data.columns= [column.capitalize() for column in data.columns]
    bt = Backtest(data, DipReboundStrategy, cash=10000, commission=.002)
    optimization_results = bt.optimize(
        dip_threshold=range(-3, 1),
        rebound_threshold=range(1, 3),
        maximize='Sharpe Ratio', # Optimize for Sharpe Ratio
        # constraint=lambda params: params.dip_threshold < params.rebound_threshold
    )
    print(optimization_results)
    bt.plot()