import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

def calculate_price_10_pips_below(price):
    pip_size = 0.0001  # Assuming the pip size is 0.0001 for this example
    pips_below = 10

    price_10_pips_below = price - (pip_size * pips_below)
    return price_10_pips_below

def calculate_price_10_pips_above(price):
    pip_size = 0.0001  # Assuming the pip size is 0.0001 for this example
    pips_above = 10

    price_10_pips_above = price + (pip_size * pips_above)
    return price_10_pips_above


def KC(data, n=19, k=2):
    """
    Calculate the Keltner Channel indicator.
    
    Parameters:
        - data: Pandas DataFrame with 'Close' column containing the closing prices.
        - n: Number of periods to use for the moving average.
        - k: Number of standard deviations to use for the channel width.
        
    Returns:
        - keltner_channel: Pandas DataFrame with 'Upper Band', 'Middle Band', and 'Lower Band' columns.
    """
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    middle_band = typical_price.rolling(n).mean()
    atr = data['High'] - data['Low']
    upper_band = middle_band + (k * atr)
    lower_band = middle_band - (k * atr)
    
    keltner_channel = pd.DataFrame({
        'Upper Band': upper_band,
        'Middle Band': middle_band,
        'Lower Band': lower_band
    })
    
    return keltner_channel

class KeltnerStochasticBollinger(Strategy):
    def init(self):
        self.keltner_channel = self.I(KC, data, 20, 1.5)
        self.stochastic = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, 28, 5, 3)
        self.bollinger_bands = self.I(talib.BBANDS, self.data.Close, 10, 1)
        self.entry_price = None
    
    def next(self):
        pips_below = calculate_price_10_pips_below(self.data.Close)
        pips_above = calculate_price_10_pips_above(self.data.Close)
        if self.data.Close[-1] < self.bollinger_bands[-1] and self.stochastic > 80 and self.data.Close[-1] < self.keltner_channel[-1]:
            # self.buy(sl=pips_below)
            self.buy()
            self.entry_price = self.data.Close
        elif self.data.Close[-1] > self.bollinger_bands[-1] and self.stochastic < 20 and self.data.Close > self.keltner_channel[-1]:
            # self.sell(sl=pips_above)
            self.sell()
            self.entry_price = self.data.Close
        # elif self.position and (self.data.Close >= self.keltner_channel[2] and self.data.Close <= self.keltner_channel[0]):
        #     self.position.close()

# Define the symbol and timeframe
if __name__ == '__main__':
    # Load the historical data
    data= pd.read_csv("./data/bitcoin/5m-2023-04-01T00:00.csv")
    data.columns= [column.capitalize() for column in data.columns]


    # Run the backtest
    bt = Backtest(data, KeltnerStochasticBollinger, cash=100000, commission=0.001)
    results = bt.run()

    # Generate and print the performance statistics
    print(results)
    bt.plot()
