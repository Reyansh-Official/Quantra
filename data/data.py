# 1. Import yfinance and pandas
import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start_date, end_date):
    ticker_data = yf.download(ticker, start=start_date, end=end_date)  #Downloads data from yahoo finance

    ticker_data.columns = ticker_data.columns.get_level_values(0)

    return ticker_data

