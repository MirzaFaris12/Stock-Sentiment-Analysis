# 📈 Stock Sentiment Analyzer with FinBERT

This is a Streamlit web app that performs sentiment analysis on recent stock-related news headlines. It uses the **FinBERT model** for financial sentiment scoring and visualizes price trends and news impact using **Plotly** charts.

---

## Features

- Fetches news articles from **Finviz**
- Uses **FinBERT** for sentiment classification (Positive / Neutral / Negative)
- Visualizes sentiment breakdown via interactive pie chart
- Highlights most impactful articles
- Fetches historical stock price (from **Twelve Data API**)
- Estimates price change following key news events

---

## How to Run the App

### 1. Clone the repository
```bash
git clone https://github.com/MirzaFaris12/Stock-Sentiment-Analysis.git
cd Stock-Sentiment-Analysis
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Twelve Data API key
Open `fetch_price.py` and replace:
```python
API_KEY = "your_actual_twelvedata_key"
```
➡️ Get a free API key from: https://twelvedata.com/signup

---

### 5. Launch the app
```bash
streamlit run main.py
```

---

## 📁 Project Structure

```
├── main.py                      # Streamlit app interface
├── fetch_news_finviz.py         # Scrapes news headlines from Finviz
├── analyze_sentiment.py         # Uses FinBERT to assign sentiment + confidence
├── fetch_price.py               # Retrieves stock price history from Twelve Data
├── requirements.txt             # All dependencies
├── README.md                    # This file
```

---

## Dependencies

- `streamlit`
- `transformers` (Hugging Face for FinBERT)
- `torch`
- `plotly`
- `pandas`
- `bs4` (BeautifulSoup)
- `requests`

Install with:
```bash
pip install -r requirements.txt
```

---

## How It Works

1. User enters a stock ticker (e.g., TSLA)
2. News headlines are scraped from Finviz
3. Each headline is scored with FinBERT
4. Sentiment stats and most impactful headlines are displayed
5. Stock price trend and post-news movement are charted

---

## Example Output

- ✅ Pie chart of sentiment distribution
- ✅ Ranked list of key headlines and confidence scores
- ✅ Closing price trend over the past month
- ✅ Table of % price change after each news event

---

## Author

Developed by **Mirza Faris**  
Prompt engineering guidance by **OpenAI ChatGPT**

---

## Support

If you encounter issues:
- Make sure your API key is valid
- Ensure dependencies are installed correctly
- Use a supported Python version (>=3.8)
