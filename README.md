# 📈 Stock Market News & Sentiment Analysis

This Streamlit app provides real-time sentiment analysis of recent stock market news along with historical stock price charts. It fetches headlines, scores them using VADER sentiment analysis, and visualizes sentiment distribution and price trends.

---

## 🔧 Features

- ✅ Fetch recent news articles for a stock ticker (via NewsAPI)
- ✅ Analyze news sentiment using VADER (Positive / Neutral / Negative)
- ✅ Display sentiment distribution via pie chart
- ✅ Display historical price data (via Twelve Data API)
- ✅ Clean, responsive Streamlit dashboard

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Replace the demo key in `fetch_price.py` with your own Twelve Data API key:
```python
API_KEY = "your_actual_key"
```
You can get a free API key at https://twelvedata.com/signup

### 4. Launch the app
```bash
streamlit run main.py
```

---

## Example Output

- Summary of news sentiment
- Interactive pie chart of article sentiment
- Line chart of daily closing prices over the past month

---

## Dependencies

- `streamlit`
- `plotly`
- `requests`
- `vaderSentiment`
- `yfinance` (optionally removed)

---

## Future Enhancements (Planned for Week 3)

- Add GPT-based summary generation
- Export sentiment results to CSV
- Add stock filtering by sector
- Compare sentiment across tickers

---

## Credits

Created by Mirza Faris  
Guided by OpenAI’s ChatGPT in prompt engineering research
