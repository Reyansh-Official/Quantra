def run_backtest(data, signals):
    start_amount = 10000
    cash = start_amount
    shares = 0
    last_price = 0

    for price, signal in zip(data["Close"], signals):
        if signal == "buy":
            if cash > price and shares == 0 :
                shares = cash // price
                cash = cash % price

        if signal == "sell":
            cash = cash + (shares * price)
            shares = 0

        if signal == "hold":
            pass

        last_price = price

    final_portfolio_value = cash + (shares * last_price)
    total_return = ((final_portfolio_value - start_amount) / start_amount) * 100

    return final_portfolio_value, total_return


