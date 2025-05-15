import requests, os
import pandas as pd
import streamlit as st

def fetch_price(ticker):
    key = st.secrets["ALPHAVANTAGE_API_KEY"]
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=compact&apikey={key}"
    r = requests.get(url)
    data = r.json().get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(data, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={"4. close": "Close"})
    df["Close"] = df["Close"].astype(float)
    return df.sort_index()

