import backtrader as bt
import talib

class BondTradingStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
    )

    def __init__(self):
        self.bond_price = self.datas[0].close
        self.rsi = bt.indicators.RSI_SMA(self.bond_price, period=self.params.rsi_period)

    def next(self):
        if not self.position:
            if self.rsi < self.params.rsi_oversold:
                self.buy()
        else:
            if self.rsi > self.params.rsi_overbought:
                self.sell()