import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class FundingRateStrategy(Strategy):
    low_funding_rate = -0.000075
    high_funding_rate = 0.000075
    
    def init(self):
        # print(self.data.Fundingrate)
        self.funding_rate = self.I(lambda x: x, self.data.Fundingrate)

    def next(self):
        # Buy when funding rate is lower than low_funding_rate
        print(self.funding_rate[-1])
        if self.funding_rate[-1] < self.low_funding_rate:
            self.buy()

        # Sell when funding rate is higher than high_funding_rate
        if self.funding_rate[-1] > self.high_funding_rate:
            self.sell()
# Load data from the CSV file
data = pd.read_csv('data/merged_df.csv', parse_dates=['datetime'], index_col='datetime')
data.columns = [column.capitalize() for column in data.columns]
print(data.columns)
data.Fundingrate = data.Fundingrate.apply(lambda x: float(x.strip('%')) / 100)


bt = Backtest(data, FundingRateStrategy, cash=1000000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()
