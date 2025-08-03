# main.py
# Streamlit app to display stock sentiment and price trends

import streamlit as st
from src.fetch_news import get_news_articles
from src.analyze_sentiment import analyze_sentiment_vader
from src.fetch_price import get_price_data
import plotly.express as px
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title="Stock Sentiment Analyzer", layout="wide")
st.title("📈 Stock Market News & Sentiment Analysis")

# --- User input ---
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL)", value="AAPL")

if st.button("Analyze"):
    with st.spinner("Fetching data and analyzing sentiment..."):
        
        # 1. Get recent news articles for the stock ticker
        articles = get_news_articles(ticker)

        if not articles:
            st.error("No news articles found. Try a different ticker.")
        else:
            # 2. Perform sentiment analysis using VADER
            df_sentiment = analyze_sentiment_vader(articles)

            # 3. Display sentiment breakdown with pie chart
            sentiment_counts = df_sentiment['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']

            fig_pie = px.pie(
                sentiment_counts,
                names='Sentiment',
                values='Count',
                title='Sentiment Distribution',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # 4. Show table of news headlines with sentiment scores
            st.subheader("📰 News Headlines and Sentiment")
            st.dataframe(df_sentiment[['title', 'published_at', 'sentiment', 'score']])

            # 5. Retrieve and plot historical stock price data
            df_price = get_price_data(ticker)
            if df_price is not None:
                fig_price = px.line(
                    df_price,
                    x='datetime',
                    y='close',
                    title=f'{ticker} Closing Prices Over Time'
                )
                st.plotly_chart(fig_price, use_container_width=True)
            else:
                st.warning("Price data not available. Check ticker symbol or API usage limits.")














