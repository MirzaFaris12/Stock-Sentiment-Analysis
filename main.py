import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from fetch_news_finviz import fetch_news_finviz
from analyze_sentiment import score_articles
from fetch_price import fetch_price

# ----- Streamlit Page Config -----
st.set_page_config(page_title="Stock Market News & Sentiment Report", layout="wide")
st.title("📈 Stock Market News & Sentiment Analysis")

# ----- Input UI -----
with st.expander("🔍 Analysis Settings"):
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
    keyword = st.text_input("Optional: Filter headlines containing this keyword (e.g., 'AI')", "")
    top_n = st.slider("Top N impactful articles to show:", 1, 20, 10)

# ----- Main Analysis Trigger -----
if st.button("Generate Report"):
    articles = fetch_news_finviz(ticker)
    if not articles:
        st.warning("⚠️ No articles found for this ticker.")
    else:
        if keyword:
            articles = [a for a in articles if keyword.lower() in a.get("title", "").lower()]

        sentiments = score_articles(articles)
        if not sentiments:
            st.warning("⚠️ Sentiment analysis failed or returned no results.")
        else:
            # Filter and sort impactful articles
            sentiments = [item for item in sentiments if item["sentiment"] != 0 and "confidence" in item]
            if not sentiments:
                st.warning("⚠️ All articles had neutral (0) sentiment or missing confidence scores.")
            else:
                # Sort by sentiment strength * confidence
                sentiments.sort(key=lambda x: abs(x["sentiment"] * x["confidence"]), reverse=True)
                sentiments = sentiments[:top_n]

                # ----- News Highlights -----
                st.subheader(f"🗞️ Sentiment Report for {ticker.upper()}")
                st.markdown("---")

                st.subheader("📰 News Highlights")
                for item in sentiments:
                    sentiment_label = ("🔴 Negative" if item['sentiment'] < -0.05 else
                                       "🟢 Positive" if item['sentiment'] > 0.05 else
                                       "🟡 Neutral")
                    confidence_text = f", Confidence: {item['confidence']:.2f}" if 'confidence' in item else ""
                    date_str = item.get("publishedAt", "N/A")
                    st.markdown(f"- **[{date_str}]** {item['title']} ({sentiment_label}{confidence_text})")

                # ----- Sentiment Summary -----
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

                # ----- Stock Price Chart -----
                st.markdown("---")
                st.subheader("📈 Stock Price Chart")
                df_price = fetch_price(ticker.upper())
                if df_price is not None:
                    fig_price = px.line(df_price, x="Date", y="Close", title=f"{ticker.upper()} - Past Month Closing Prices")
                    st.plotly_chart(fig_price, use_container_width=True)

                    with st.expander("View Raw Price Data"):
                        st.dataframe(df_price)

                    # ----- Price Change After News (Order-Based) -----
                    df_price_sorted = df_price.sort_values("Date", ascending=False).reset_index(drop=True)
                    enriched = []
                    num_articles = min(len(sentiments), len(df_price_sorted) - 1)

                    for i in range(num_articles):
                        article = sentiments[i]
                        price_today = df_price_sorted.loc[i, "Close"]
                        price_next = df_price_sorted.loc[i + 1, "Close"]
                        change = (price_next - price_today) / price_today * 100
                        enriched.append({
                            "Title": article["title"],
                            "Date": article.get("publishedAt", "N/A"),
                            "Sentiment": article["sentiment"],
                            "Confidence": article["confidence"],
                            "Price at Publish": price_today,
                            "Price Next Day": price_next,
                            "Change (%)": round(change, 2)
                        })

                    if enriched:
                        st.markdown("---")
                        st.subheader("💹 Price Change Table After News (Sorted by Impact Score)")
                        df_enriched = pd.DataFrame(enriched)
                        df_enriched = df_enriched.sort_values(by="Sentiment", key=abs, ascending=False)

                        def highlight_sentiment(row):
                            color = ""  # default
                            if row['Sentiment'] > 0.05:
                                color = "background-color: #d1f7d1;"
                            elif row['Sentiment'] < -0.05:
                                color = "background-color: #f7d1d1;"
                            return [color] * len(row)

                        st.dataframe(df_enriched.style.apply(highlight_sentiment, axis=1), use_container_width=True)
                    else:
                        st.warning("⚠️ Not enough price data to show price changes.")
                else:
                    st.warning("⚠️ Could not retrieve price data. Check the ticker symbol or try again later.")















