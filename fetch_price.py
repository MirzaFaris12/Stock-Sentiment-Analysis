import yfinance as yf
import pandas as pd

def fetch_price(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", group_by="ticker")
        if df.empty:
            return None
        df = df.rename_axis("Date").reset_index()

        # ⬇️ Flatten MultiIndex columns if they exist
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        return df[["Date", "Close"]]
    except Exception:
        return None





