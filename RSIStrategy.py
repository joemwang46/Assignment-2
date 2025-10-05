from PriceLoader import MarketDataPoint
from BenchmarkStrategy import Strategy
import pandas as pd

class RSIStrategy(Strategy):
    def __init__(self, lookback=14):
        self._lookback = lookback
        self._prices = []

    def generate_signals(self, tick):
        self._prices.append(tick.price)

        if len(self._prices) < self._lookback + 1:
            return 0

        series = pd.Series(self._prices[-(self._lookback + 1):])
        delta = series.diff().dropna()
        gain = delta.clip(lower=0).mean()
        loss = -delta.clip(upper=0).mean()
        
        if loss != 0:
            rsi = 100 - (100 / (1 + gain / loss))
        else:
            rsi = 100

        if rsi < 30:
            return 1
        else:
            return 0
