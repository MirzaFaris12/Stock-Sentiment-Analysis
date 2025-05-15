import yfinance as yf
import pandas as pd

def fetch_price(ticker):
    data = yf.download(ticker, period="1mo", interval="1d")
    if data.empty:
        return None
    return data[["Close"]]


