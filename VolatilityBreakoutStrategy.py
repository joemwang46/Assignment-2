from abc import ABC, abstractmethod
from PriceLoader import MarketDataPoint
from BenchmarkStrategy import Strategy

class VolatilityBreakoutStrategy(Strategy):
    def __init__(self, lookback=20, multiplier=2):
        self._lookback = lookback
        self._multiplier = multiplier
        self._prices = []

    def generate_signals(self, tick):
        self._prices.append(tick.price)
        
        if len(self._prices) < self._lookback:
            return 0
        
        else:
            recent_prices = self._prices[-self._lookback:]
            mean = sum(recent_prices) / self._lookback
            squared_diffs = [(p - mean) ** 2 for p in recent_prices]
            variance = sum(squared_diffs) / self._lookback
            rolling_std_dev = variance ** 0.5

            if tick.price > rolling_std_dev:
                return 1
            else:
                return 0
            