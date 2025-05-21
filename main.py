import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from fetch_news import fetch_news
from analyze_finbert import score_with_finbert
from fetch_price import fetch_price

st.set_page_config(page_title="Stock Market News & Sentiment Report")
st.title("📈 Stock Market News & Sentiment Analysis")

st.markdown("Select a stock ticker to generate a sentiment report based on recent news headlines.")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
keyword = st.text_input("Optional: Filter headlines containing this keyword (e.g., 'AI')", "")

if st.button("Generate Report"):
    articles = fetch_news(ticker)
    if keyword:
        articles = [a for a in articles if keyword.lower() in a.get("title", "").lower()]

    titles = [a.get("title", "") for a in articles]
    sentiments = score_with_finbert(titles)

    st.subheader(f"Report for {ticker.upper()}")
    st.markdown("### News Highlights")
    for item in sentiments:
        label = item['sentiment']
        emoji = "🟢" if label == "Positive" else "🔴" if label == "Negative" else "🟡"
        st.markdown(f"- {item['title']} ({emoji} {label}, Confidence: {item['confidence']:.2f})")

    st.markdown("### Summary")
    total = len(sentiments)
    pos = sum(1 for x in sentiments if x['sentiment'] == "Positive")
    neg = sum(1 for x in sentiments if x['sentiment'] == "Negative")
    neu = sum(1 for x in sentiments if x['sentiment'] == "Neutral")
    st.write(f"Out of {total} articles: 🟢 {pos} Positive, 🟡 {neu} Neutral, 🔴 {neg} Negative")

    # Sentiment distribution pie chart
    labels = ["Positive", "Neutral", "Negative"]
    values = [pos, neu, neg]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig, use_container_width=True)

    # Stock Price Chart
    df_price = fetch_price(ticker.upper())
    st.write("📊 Raw price data:", df_price)
    if df_price is not None:
        fig_price = px.line(df_price, x="Date", y="Close", title=f"{ticker.upper()} - Past Month Closing Prices")
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning("⚠️ Could not retrieve price data. Check the ticker symbol or try again later.")



