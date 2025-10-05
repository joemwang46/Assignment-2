from PriceLoader import MarketDataPoint
from BenchmarkStrategy import Strategy
import pandas as pd

class MACDStrategy(Strategy):
    def __init__(self, fast=12, slow=26, signal=9):
        self._fast = fast
        self._slow = slow
        self._signal = signal
        self._prices = []

    def generate_signals(self, tick):
        self._prices.append(tick.price)

        if len(self._prices) < self._slow + self._signal:
            return 0
        
        ema_fast = pd.Series(self._prices).ewm(span=self._fast, adjust=False).mean().iloc[-1]
        ema_slow = pd.Series(self._prices).ewm(span=self._slow, adjust=False).mean().iloc[-1]
        macd = ema_fast - ema_slow

        signal_line = pd.Series([ema_fast - ema_slow for ema_fast, ema_slow in zip(
            pd.Series(self._prices).ewm(span=self._fast, adjust=False).mean(),
            pd.Series(self._prices).ewm(span=self._slow, adjust=False).mean()
        )]).ewm(span=self._signal, adjust=False).mean().iloc[-1]
        
        if macd > signal_line:
            return 1
        else:
            return 0
