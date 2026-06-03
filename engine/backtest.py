import numpy as np
import pandas as pd


def run_backtest(data, signals):
    start_amount = 10000

    # Convert signals to 1 (buy), 0 (sell), NaN (hold)
    positions = pd.Series(np.where(signals == "buy", 1, np.where(signals == "sell", 0, np.nan)))

    # Forward fill NaNs — carry last known position forward. Start at 0 before any buy signal.
    positions = positions.ffill().fillna(0)

    # Calculate how much the stock price moved each day as a percentage
    daily_market_returns = data["Close"].pct_change()

    # Multiply by positions — 1 means you captured that day's move, 0 means you missed it
    strategy_returns = positions * daily_market_returns

        if signal == "hold":
            pass

        last_price = price

    final_portfolio_value = cash + (shares * last_price)
    total_return = ((final_portfolio_value - start_amount) / start_amount) * 100

    return final_portfolio_value, total_return


