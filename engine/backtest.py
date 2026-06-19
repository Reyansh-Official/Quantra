import numpy as np
import pandas as pd


def run_backtest(data, signals):
    start_amount = 10000

    # Convert signals to 1 (buy), 0 (sell), NaN (hold)
    positions = pd.Series(
        np.where(signals == "buy", 1, np.where(signals == "sell", 0, np.nan)),
        index=data.index
    )

    # Forward fill NaNs — carry last known position forward. Start at 0 before any buy signal.
    positions = positions.ffill().fillna(0)

    # Calculate how much the stock price moved each day as a percentage
    daily_market_returns = data["Close"].pct_change()

    # Multiply by positions — 1 means you captured that day's move, 0 means you missed it
    strategy_returns = positions.shift(1) * daily_market_returns
    strategy_returns = strategy_returns.fillna(0)

    # Add 1 to each return, then cumprod compounds them — each day builds on the last
    compounded = (1 + strategy_returns).cumprod()

    # Apply compounded growth to starting capital — gives portfolio value for every single day
    portfolio_value = compounded * start_amount

    # Grab the last day — that's your final portfolio value
    final_portfolio_value = portfolio_value.iloc[-1]

    # Calculate percentage gain from start to finish
    total_return = (final_portfolio_value - start_amount) / start_amount * 100

    df = pd.DataFrame({
        'Close': data["Close"],
        'Signals': signals,
    }, index=data.index)

    df = df.reset_index()
    df.columns = ['Date' if col in ['index', 'Date'] else col for col in df.columns]

    records = df.to_dict('records')

    trades = []
    in_position = False
    entry_date = None
    entry_price = None

    for row in records:
        current_date = row["Date"]
        current_close = row["Close"]
        current_signal = row["Signals"]

        if current_signal == "buy" and not in_position:
            in_position = True
            entry_price = current_close
            entry_date = current_date

        elif current_signal == "sell" and in_position:
            exit_date = current_date
            exit_price = current_close

            # Calculate target metrics
            profit_dollars = exit_price - entry_price
            return_pct = (profit_dollars / entry_price) * 100
            duration_days = (exit_date - entry_date).days

            trades.append({
                'entry_date': entry_date,
                'entry_price': entry_price,
                'exit_date': exit_date,
                'exit_price': exit_price,
                'profit_dollars': profit_dollars,
                'return_pct': return_pct,
                'duration_days': duration_days,
                'exit_reason': 'signal'
            })

            #Resetting state memory for the next trade
            in_position = False
            entry_price = None
            entry_date = None

    # ==========================================
    # FORCE-CLOSE LOGIC
    # ==========================================

    if in_position and records:
        last_row = records[-1]
        exit_date = last_row['Date']
        exit_price = last_row['Close']

        profit_dollars = exit_price - entry_price
        return_pct = (profit_dollars / entry_price) * 100
        duration_days = (exit_date - entry_date).days

        trades.append({
            'entry_date': entry_date,
            'entry_price': entry_price,
            'exit_date': exit_date,
            'exit_price': exit_price,
            'profit_dollars': profit_dollars,
            'return_pct': return_pct,
            'duration_days': duration_days,
            'exit_reason': 'forced_end'
        })

    # Convert the completed trade history list into a pandas DataFrame
    trades_df = pd.DataFrame(trades)

    # Total number of trades
    total_trades = len(trades_df)

    if total_trades > 0:

        # If profit is greater than 0, then the trade is considered as a win, else it is a loss
        winning_trades = int((trades_df['profit_dollars'] > 0).sum())
        losing_trades = int((trades_df['profit_dollars'] < 0).sum())

        metrics = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,

            # Win rate of trades
            'win_rate': (winning_trades / total_trades),

            # Average trade duration
            'avg_trade_duration_days': float(trades_df['duration_days'].mean()),

            # Best and worst return percentages for trades
            'best_trade': float(trades_df['return_pct'].max()),
            'worst_trade': float(trades_df['return_pct'].min()),

            # Average return percentages for winning and losing trades
            'avg_winning_trade': float(trades_df.loc[trades_df['profit_dollars'] > 0, 'return_pct'].mean()) if winning_trades > 0 else 0.0,
            'avg_losing_trade': float(trades_df.loc[trades_df['profit_dollars'] < 0, 'return_pct'].mean()) if losing_trades > 0 else 0.0
        }

    else:
        metrics = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'avg_trade_duration_days': 0.0,
            'best_trade': 0.0,
            'worst_trade': 0.0,
            'avg_winning_trade': 0.0,
            'avg_losing_trade': 0.0
        }

    return final_portfolio_value, total_return, trades_df, metrics

