from abc import ABC, abstractmethod
from PriceLoader import MarketDataPoint

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class BenchmarkStrategy(Strategy):
    def __init__(self, max_purchases=10):
        self.max_purchases = max_purchases
        self._prices = []

    def generate_signals(self, tick):
        self._prices.append(tick.price)
        
        if self.max_purchases <= 0:
            return 0
        
        else:
            return 1
