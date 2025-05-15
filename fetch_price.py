import yfinance as yf
import pandas as pd

def fetch_price(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d")
        if df.empty:
            return None
        df = df.reset_index()
        return df[["Date", "Close"]]
    except Exception as e:
        return None



