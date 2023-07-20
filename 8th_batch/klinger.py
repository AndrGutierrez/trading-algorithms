import talib
from backtesting import Strategy, Backtest
import pandas as pd
from backtesting.lib import crossover

import talib

def calculate_klinger_volume_oscillator(high, low, close, volume, short_period=34, long_period=55, signal_period=13):
    key_price_t = [(high[i] + low[i] + close[i])/3 for i in range(len(high))]
    key_price_t_minus_1 = [(high[i-1] + low[i-1] + close[i-1])/3 for i in range(len(high))]

    trend = volume if key_price_t > key_price_t_minus_1 else [-i for i in volume]
    # trend=volume
    kvo = talib.EMA(trend, timeperiod=short_period) - talib.EMA(trend, timeperiod=long_period)
    kvo_signal = talib.EMA(kvo, timeperiod=signal_period)

    return kvo, kvo_signal

class KlingerOscillator(Strategy):
    short_period=34 
    long_period=55
    def init(self):
        # Calculate the Klinger Oscillator
        self.klinger_oscillator, self.signal = self.I(
            calculate_klinger_volume_oscillator,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            self.short_period,
            self.long_period,
        )

    def next(self):
        # If the KO is greater than zero and the previous value was less than zero, buy
        if crossover(self.klinger_oscillator, self.signal):
            # self.buy(tp=self.data.Close[-1]*1.1, sl=self.data.Close[-1]*.97)
            # self.buy(size=2)
            # self.buy(size=1)
            self.buy()

        # If the KO is less than zero and the previous value was greater than zero, sell
        elif self.signal[-1]> self.klinger_oscillator[-1]:
            self.sell(size=2)
            # self.sell()

if __name__=="__main__":
    data=pd.read_csv("./data/ethereum/1h-2022-01-01T00:00.csv")
    data.columns=[column.capitalize() for column in data.columns]
    bt=Backtest(data, KlingerOscillator, cash=100000, commission=.002)
    # stats=bt.run()
    stats=bt.optimize(short_period=range(10, 50, 5), long_period=range(50, 100, 5), maximize='Equity Final [$]')
    print(stats)
    bt.plot()
