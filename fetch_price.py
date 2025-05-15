import yfinance as yf
import pandas as pd

def fetch_price(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d", group_by="ticker", progress=False)

        # Retry once with longer period if failed
        if df is None or df.empty:
            df = yf.download(ticker, period="6mo", interval="1d", progress=False)

        if df is None or df.empty:
            return None

        df = df.rename_axis("Date").reset_index()
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        return df[["Date", "Close"]]
    except Exception as e:
        return None





