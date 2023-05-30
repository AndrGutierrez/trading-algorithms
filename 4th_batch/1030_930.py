import backtesting
import talib
import pandas as pd
class SMATradingStrategy(backtesting.Strategy):
    stop_loss_pct = 5
    take_profit_pct = 1
    def init(self):
        self.sma5 = self.I(talib.SMA, self.data.Close, timeperiod=5)
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.entry_hour = 9
        self.exit_hour = 10

    def next(self):
        hour= pd.Timestamp(self.data.Datetime[-1]).to_pydatetime().hour
        if self.position:
            # Si ya tenemos una posición abierta, comprobamos si debemos cerrarla
            if hour >= self.exit_hour:
                self.position.close()
        else:
            # Si no tenemos una posición abierta, comprobamos si debemos abrirla
            if hour >= self.entry_hour and self.sma5[-1] < self.sma20[-1]:
                self.buy(
                    size=1,
                    sl=self.data.Close[-1] * (1 - (self.stop_loss_pct / 1000)),
                    tp=self.data.Close[-1] * (1 + (self.take_profit_pct / 100))
                )

if __name__ == '__main__':
    data= pd.read_csv('./data/bitcoin/30m-2022-06-01T00:00.csv')
    data.columns=[column.capitalize() for column in data.columns]
    data=data.dropna()
    bt = backtesting.Backtest(data, SMATradingStrategy, cash=100000)
    result = bt.optimize(
        maximize='Equity Final [$]',
        stop_loss_pct=range(5, 20),
        take_profit_pct=range(1, 10)
    )
    bt.plot()