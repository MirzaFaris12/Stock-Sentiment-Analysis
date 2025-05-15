import requests
import pandas as pd

def fetch_price(ticker):
    API_KEY = "f5241776c6084beabd6f7563fdf27ada"
    url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=30&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "values" not in data:
            return None

        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["close"] = df["close"].astype(float)
        df = df.rename(columns={"datetime": "Date", "close": "Close"})
        return df[["Date", "Close"]].sort_values("Date")
    except Exception:
        return None






