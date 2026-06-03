"""
A moving average smooths out price data by averaging the last N days.

10-day MA — average of the last 10 closing prices. Reacts quickly to price changes.
50-day MA — average of the last 50 closing prices. Reacts slowly, shows the longer trend.

The crossover signal:

When the 10-day MA crosses above the 50-day MA — the short term trend is rising above the long term trend → BUY
When the 10-day MA crosses below the 50-day MA → SELL
Otherwise → HOLD

"""

from strategies.base import Strategy
import numpy as np

class MACrossover(Strategy):

    def __init__(self, short_window=10, long_window=50):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        short_ma = data["Close"].rolling(self.short_window).mean()
        long_ma = data["Close"].rolling(self.long_window).mean()
        signals = np.where(short_ma > long_ma, "buy", np.where(short_ma < long_ma, "sell", "hold"))
        return signals

