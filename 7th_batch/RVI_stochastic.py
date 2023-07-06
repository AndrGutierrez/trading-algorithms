from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from talib import STOCH 
from calculate_rvi import calculate_rvi

class RVIStochastic(Strategy):
    stochastic_high=80
    stochastic_low=30
    def init(self):
        self.rvi = self.I(calculate_rvi, self.data.Close)
        self.k, self.d = self.I(STOCH, self.data.High, self.data.Low, self.data.Close)
    def next(self):
        # stochastic_overbought = crossover(self.k, self.d) or self.k[-2] > self.stochastic_high
        stochastic_overbought = self.k[-1]> self.d[-1] or self.k[-1] > self.stochastic_high
        stochastic_oversold = self.k[-1] < self.stochastic_low
        rvi_overbought = self.rvi[-1] > 0.7
        rvi_oversold = self.rvi[-1] < 0.3
        # print(self.rvi[-1])
        if stochastic_oversold and rvi_oversold:
            # self.buy(sl=self.data.Close[-1]*0.95, tp=self.data.Close[-1]*1.2)
            self.buy()
        elif stochastic_overbought or rvi_overbought:
            self.sell()

    
if __name__ == "__main__":
    # data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
    data=pd.read_csv('./data/bitcoin/1h-2022-01-01T00:00.csv')
    data.columns = [column.capitalize() for column in data.columns]
    bt = Backtest(data, RVIStochastic, cash=100000, commission=.002)
    # bt.run()
    # stats=bt.optimize(maximize="Equity Final [$]", stochastic_high=range(60, 80, 5), stochastic_low=range(50, 20, 5))
    # stats=bt.optimize(maximize="Equity Final [$]", stochastic_high=range(60, 80, 5), stochastic_low=range(20, 50, 5))
    stats=bt.run()
    print(stats)
    bt.plot()
