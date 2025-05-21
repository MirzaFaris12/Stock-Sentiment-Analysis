import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from dateutil.parser import parse as parse_date

from fetch_news import fetch_news
from analyze_sentiment import score_articles
from fetch_price import fetch_price

st.set_page_config(page_title="Stock Market News & Sentiment Report")
st.title("📈 Stock Market News & Sentiment Analysis")

st.markdown("Select a stock ticker to generate a sentiment report based on recent news headlines.")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
keyword = st.text_input("Optional: Filter headlines containing this keyword (e.g., 'AI')", "")

# Date range inputs
st.markdown("Optional: Filter news by publication date range")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
with col2:
    end_date = st.date_input("End Date", datetime.date.today())

if st.button("Generate Report"):
    
    # Convert timestamps to datetime
    for item in sentiments:
        item["publishedAt"] = pd.to_datetime(item.get("publishedAt"))

    df_sentiment = pd.DataFrame(sentiments)
    df_sentiment["date"] = df_sentiment["publishedAt"].dt.date

    # Average sentiment per day
    daily_sentiment = df_sentiment.groupby("date")["sentiment"].mean().reset_index()

    # Plot sentiment over time
    fig_timeline = px.line(daily_sentiment, x="date", y="sentiment", markers=True, title="🕒 Sentiment Trend Over Time")
    fig_timeline.update_layout(xaxis_title="Date", yaxis_title="Average Sentiment")
    st.plotly_chart(fig_timeline, use_container_width=True)

    articles = fetch_news(ticker)
    if keyword:
        articles = [a for a in articles if keyword.lower() in a.get("title", "").lower()]

    # Date filtering
    articles = [
        a for a in articles
        if 'publishedAt' in a and start_date <= parse_date(a['publishedAt']).date() <= end_date
    ]

    sentiments = score_articles(articles)

    st.subheader(f"Report for {ticker.upper()}")
    st.markdown("### News Highlights")
    for item in sentiments:
        sentiment_label = ("🔴 Negative" if item['sentiment'] < -0.05 else
                           "🟢 Positive" if item['sentiment'] > 0.05 else
                           "🟡 Neutral")
        confidence_text = f", Confidence: {item['confidence']:.2f}" if 'confidence' in item else ""
        st.markdown(f"- {item['title']} ({sentiment_label}{confidence_text})")

    st.markdown("### Summary")
    total = len(sentiments)
    pos = sum(1 for x in sentiments if x['sentiment'] > 0.05)
    neg = sum(1 for x in sentiments if x['sentiment'] < -0.05)
    neu = total - pos - neg
    st.write(f"Out of {total} articles: 🟢 {pos} Positive, 🟡 {neu} Neutral, 🔴 {neg} Negative")

    # Count sentiment types
    labels = ["Positive", "Neutral", "Negative"]
    values = [
        sum(1 for x in sentiments if x['sentiment'] > 0.05),
        sum(1 for x in sentiments if -0.05 <= x['sentiment'] <= 0.05),
        sum(1 for x in sentiments if x['sentiment'] < -0.05),
    ]

    # Plot pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig, use_container_width=True)

    # Stock Price Chart using yfinance or alternative
    df_price = fetch_price(ticker.upper())
    st.write("📊 Raw price data:", df_price)
    if df_price is not None:
        fig_price = px.line(df_price, x="Date", y="Close", title=f"{ticker.upper()} - Past Month Closing Prices")
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning("⚠️ Could not retrieve price data. Check the ticker symbol or try again later.") // this is my full current main.py update it so i can copy n paste





