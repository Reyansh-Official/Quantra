from data.data import get_stock_data
from strategies.ma_crossover import MACrossover
from engine.backtest import run_backtest
from analytics.benchmark import buy_and_hold

apple_data = get_stock_data('AAPL', "2015-01-01", "2025-12-31" )
strategy = MACrossover()
signals = strategy.generate_signals(apple_data)
print(signals.value_counts())

final_portfolio_value, total_return, trades_df, metrics  = run_backtest(apple_data,signals)

print(f"Final Portfolio Value: {final_portfolio_value}")
print(f"Total Return: {total_return}")
print(trades_df.head())
print(f"Total Trades: {len(trades_df)}")

print(f"Winning Trades              : {metrics['winning_trades']}")
print(f"Losing Trades               : {metrics['losing_trades']}")

print(f"Win Rate                    : {metrics['win_rate'] * 100:.2f}%")
print(f"Average Duration (Days)     : {metrics['avg_trade_duration_days']:.1f} days")

print("---------------------------------------------")
print(f"Best Trade Performance      : {metrics['best_trade']:.2f}%")
print(f"Worst Trade Performance     : {metrics['worst_trade']:.2f}%")
print(f"Avg Winning Trade           : {metrics['avg_winning_trade']:.2f}%")
print(f"Avg Losing Trade            : {metrics['avg_losing_trade']:.2f}%")
print("---------------------------------------------")

final_portfolio, buy_and_hold_return = buy_and_hold(apple_data, 10000)

print(f"Buy and Hold Final Portfolio Value: {final_portfolio}")
print(f"Buy and Hold Total Return: {buy_and_hold_return}%") 