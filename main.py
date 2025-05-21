import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from dateutil.parser import parse as parse_date
from datetime import timedelta

from fetch_news import fetch_news
from analyze_sentiment import score_articles
from fetch_price import fetch_price

st.set_page_config(page_title="Stock Market News & Sentiment Report", layout="wide")
st.title("📈 Stock Market News & Sentiment Analysis")

with st.expander("🔍 Analysis Settings"):
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
    keyword = st.text_input("Optional: Filter headlines containing this keyword (e.g., 'AI')", "")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.date.today())

if st.button("Generate Report"):
    articles = fetch_news(ticker)
    if not articles:
        st.warning("⚠️ No articles found for this ticker.")
    else:
        if keyword:
            articles = [a for a in articles if keyword.lower() in a.get("title", "").lower()]

        articles = [
            a for a in articles
            if 'publishedAt' in a and start_date <= parse_date(a['publishedAt']).date() <= end_date
        ]

        sentiments = score_articles(articles)
        if not sentiments:
            st.warning("⚠️ Sentiment analysis failed or returned no results.")
        else:
            st.subheader(f"🗞️ Sentiment Report for {ticker.upper()}")
            st.markdown("---")

            st.subheader("📰 News Highlights")
            for item in sentiments:
                sentiment_label = ("🔴 Negative" if item['sentiment'] < -0.05 else
                                   "🟢 Positive" if item['sentiment'] > 0.05 else
                                   "🟡 Neutral")
                confidence_text = f", Confidence: {item['confidence']:.2f}" if 'confidence' in item else ""
                st.markdown(f"- {item['title']} ({sentiment_label}{confidence_text})")

            st.markdown("---")
            st.subheader("📊 Summary Statistics")
            total = len(sentiments)
            pos = sum(1 for x in sentiments if x['sentiment'] > 0.05)
            neg = sum(1 for x in sentiments if x['sentiment'] < -0.05)
            neu = total - pos - neg

            c1, c2, c3 = st.columns(3)
            c1.metric("🟢 Positive", pos)
            c2.metric("🟡 Neutral", neu)
            c3.metric("🔴 Negative", neg)

            labels = ["Positive", "Neutral", "Negative"]
            values = [pos, neu, neg]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader("📈 Stock Price Chart")
            df_price = fetch_price(ticker.upper())
            if df_price is not None:
                fig_price = px.line(df_price, x="Date", y="Close", title=f"{ticker.upper()} - Past Month Closing Prices")
                st.plotly_chart(fig_price, use_container_width=True)

                with st.expander("View Raw Price Data"):
                    st.dataframe(df_price)

                # 📉 Price change after each article
                enriched = []
                df_price["Date"] = pd.to_datetime(df_price["Date"])
                df_price_sorted = df_price.sort_values("Date")
                for article in sentiments:
                    if "publishedAt" not in article:
                        continue
                    try:
                        pub_date = pd.to_datetime(article["publishedAt"]).date()
                    except Exception:
                        continue

                    price_today_row = df_price_sorted[df_price_sorted["Date"].dt.date <= pub_date].tail(1)
                    price_next_row = df_price_sorted[df_price_sorted["Date"].dt.date > pub_date].head(1)

                    if not price_today_row.empty and not price_next_row.empty:
                        price_today = price_today_row["Close"].values[0]
                        price_next = price_next_row["Close"].values[0]
                        change = (price_next - price_today) / price_today * 100
                        enriched.append({
                            "Title": article["title"],
                            "Sentiment": article["sentiment"],
                            "Published Date": pub_date,
                            "Price at Publish": price_today,
                            "Price Next Day": price_next,
                            "Change (%)": round(change, 2)
                        })

                if enriched:
                    st.markdown("---")
                    st.subheader("💹 Price Change After News")
                    st.dataframe(pd.DataFrame(enriched))
            else:
                st.warning("⚠️ Could not retrieve price data. Check the ticker symbol or try again later.")







