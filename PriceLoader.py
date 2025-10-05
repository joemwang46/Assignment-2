import yfinance as yf
import os
import pandas as pd
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class PriceLoader:
    def __init__(self, ticker: str, start: str, end: str):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.datapoints = []

    def fetch_prices(self):
        filename = f"{self.ticker}.parquet"

        if os.path.exists(filename):
            print(f"Loading {filename} from disk...")
            data = pd.read_parquet(filename)
        else:
            print(f"No local file found. Downloading data for {self.ticker}...")
            data = yf.download(self.ticker, start=self.start, end=self.end)

            if data.isna().any().any():
                pass
            else:
                data.to_parquet(filename)

        for date, row in data.iterrows():
            datapoint = MarketDataPoint(
                timestamp=date.to_pydatetime(),
                symbol=self.ticker,
                price=float(row["Close"])
            )
            self.datapoints.append(datapoint)

        return self.datapoints


class Order:
    def __init__(self, symbol: str, quantity: int, price: float, status: str):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = status
    
    def validate(self):
        if self.quantity is None or self.price is None:
            raise OrderError("Order missing quantity or price")
        if self.quantity == 0:
            raise OrderError("Order quantity cannot be zero")
        if self.quantity < 0:
            raise OrderError("Order quantity cannot be negative")
        if self.price <= 0:
            raise OrderError("Order price must be positive")

class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass
