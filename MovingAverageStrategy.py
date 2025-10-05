from abc import ABC, abstractmethod
from PriceLoader import MarketDataPoint
from BenchmarkStrategy import Strategy

class MovingAverageStrategy(Strategy):
    def __init__(self, short_window=20, long_window=50):
        self._short_window = short_window
        self._long_window = long_window
        self._prices = []

    def generate_signals(self, tick):
        self._prices.append(tick.price)
        
        if len(self._prices) < self._long_window:
            return 0
        
        else:
            short_moving_avg = sum(self._prices[-1*self._short_window:]) / self._short_window
            long_moving_avg = sum(self._prices[-1*self._long_window:]) / self._long_window

            if short_moving_avg > long_moving_avg:
                return 1
            else:
                return 0
