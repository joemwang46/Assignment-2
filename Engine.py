from PriceLoader import Order, OrderError, ExecutionError
import matplotlib.pyplot as plt

class StrategyExecutor:
    def __init__(self, signal_list=None, order_list=None):
        self._signal_list = signal_list or []
        self._order_list = order_list or []

    def execute(self, strategy, data=None) -> list:
        data = data or []
        signals = []
        for dp in data:
            try:
                sig = strategy.generate_signals(dp)
            except Exception as e:
                print(f"Strategy error at {dp.timestamp}: {e}")
                continue
            if sig == 1:
                signals.append(("BUY", dp.symbol, 1, dp.price))
            else:
                signals.append(("HOLD", dp.symbol, 1, dp.price))
        self._signal_list = signals
        return signals
    
    def return_orders(self):
        orders = []
        for signal in self._signal_list:
            try:
                o = Order(signal[1], signal[2], signal[3], signal[0])
                o.validate()
                orders.append(o)
            except OrderError as oe:
                print(f"OrderError for {signal[1]}: {oe}")
            except Exception as e:
                print(f"Unexpected error creating order for {signal[1]}: {e}")
        self._order_list = orders
        return orders


class Portfolio:
    def __init__(self, positions=None, cash=1_000_000.0):
        self.positions = positions or {}
        self.cash = cash
        self.time = []
        self.signal = []
        self.cash_history = []
        self.value_history = []

    def execute_orders(self, order_lists=None, price_lists=None):
        if not order_lists:
            return
        price_lists = price_lists or {}
        max_len = max((len(ol) for ol in order_lists.values()), default=0)

        for i in range(max_len):
            buy_signal = 0
            for ticker, order_list in order_lists.items():
                if i >= len(order_list):
                    continue
                o = order_list[i]
                try:
                    if o.status == "BUY":
                        cost = o.price * o.quantity
                        if self.cash >= cost and o.quantity > 0 and o.price > 0:
                            pos = self.positions.get(o.symbol, {"quantity": 0, "avg_price": 0.0})
                            pos["quantity"] += o.quantity
                            pos["avg_price"] = o.price
                            self.positions[o.symbol] = pos
                            self.cash -= cost
                            buy_signal = 1
                except ExecutionError as ee:
                    print(f"ExecutionError: {ee}")
                except Exception as e:
                    print(f"Unexpected error executing order at t={i}: {e}")

            self.time.append(i)
            self.signal.append(buy_signal)
            self.cash_history.append(self.cash)

            value = self.cash
            for sym, pos in self.positions.items():
                px_list = price_lists.get(sym, [])
                px = px_list[i] if i < len(px_list) else pos["avg_price"]
                value += pos["quantity"] * px
            self.value_history.append(value)

    def return_portfolio_value(self):
        return self.value_history[-1] if self.value_history else self.cash


def plot_portfolio(pf: Portfolio):
    plt.figure(figsize=(8, 4))
    plt.plot(pf.time, pf.signal, drawstyle="steps-post")
    plt.title("Buy Signal (0 or 1)")
    plt.xlabel("Time index (i)")
    plt.ylabel("Signal")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.plot(pf.time, pf.cash_history)
    plt.title("Cash Balance Over Time")
    plt.xlabel("Time index (i)")
    plt.ylabel("Cash ($)")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.plot(pf.time, pf.value_history)
    plt.title("Total Portfolio Value Over Time")
    plt.xlabel("Time index (i)")
    plt.ylabel("Value ($)")
    plt.grid(True)
    plt.show()
