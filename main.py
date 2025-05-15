import streamlit as st
from fetch_news import fetch_news
from analyze_sentiment import score_articles

st.set_page_config(page_title="Stock Market News & Sentiment Report")
st.title("📈 Stock Market News & Sentiment Analysis")

st.markdown("Select a stock ticker to generate a sentiment report based on recent news headlines.")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")

if st.button("Generate Report"):
    articles = fetch_news(ticker)
    sentiments = score_articles(articles)

    st.subheader(f"Report for {ticker.upper()}")
    st.markdown("### News Highlights")
    for item in sentiments:
        sentiment_label = ("🔴 Negative" if item['sentiment'] < -0.05 else
                           "🟢 Positive" if item['sentiment'] > 0.05 else
                           "🟡 Neutral")
        st.markdown(f"- {item['title']} ({sentiment_label})")

    st.markdown("### Summary")
    total = len(sentiments)
    pos = sum(1 for x in sentiments if x['sentiment'] > 0.05)
    neg = sum(1 for x in sentiments if x['sentiment'] < -0.05)
    neu = total - pos - neg
    st.write(f"Out of {total} articles: 🟢 {pos} Positive, 🟡 {neu} Neutral, 🔴 {neg} Negative")
