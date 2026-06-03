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
import pandas as pd

class MACrossover(Strategy):

    def __init__(self, short_window=10, long_window=50):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        short_ma = data["Close"].rolling(self.short_window).mean()
        long_ma = data["Close"].rolling(self.long_window).mean()
        buy_condition = (short_ma > long_ma) &  (short_ma.shift(1) <= long_ma.shift(1))
        sell_condition = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
        raw_signals = np.where(buy_condition, "buy", np.where(sell_condition, "sell", "hold"))
        signals = pd.Series(raw_signals, index=data.index)
        return signals

