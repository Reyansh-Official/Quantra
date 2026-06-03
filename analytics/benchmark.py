def buy_and_hold(data, start_amount = 10000):
    closing_price_day_one = data["Close"].iloc[0]
    closing_price_last_day = data["Close"].iloc[-1]

    multiplier = closing_price_last_day / closing_price_day_one
    final_portfolio_value = multiplier * start_amount

    buy_and_hold_return = (final_portfolio_value - start_amount) / start_amount * 100

    return final_portfolio_value, buy_and_hold_return