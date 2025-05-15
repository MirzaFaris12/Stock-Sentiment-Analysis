import yfinance as yf
import pandas as pd

def fetch_price(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d")
        if df.empty:
            return None
        df = df.rename_axis("Date").reset_index()  # ⬅️ This fixes the error
        return df[["Date", "Close"]]
    except Exception:
        return None




