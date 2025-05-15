import requests, os

def fetch_news(ticker):
    key = os.getenv("NEWS_API_KEY", "")
    if not key:
        import streamlit as st
        key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={key}&language=en"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles[:10]
