# Import requests to handle HTTP requests for API or web scraping
import requests

# Import BeautifulSoup for parsing HTML content
from bs4 import BeautifulSoup

from datetime import datetime

# Function to fetch recent news articles from Finviz
def fetch_news_finviz(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    r = requests.get(url, headers=headers)

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    news_table = soup.find('table', class_='fullview-news-outer')

    if news_table is None:
        # Return empty list if no news table is found
        return []

    rows = news_table.find_all('tr')
    articles = []

    # Format today's date string for timestamp matching
    today_str = datetime.now().strftime("%b-%d-%y")  # e.g., Jun-11-25

    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue

        time_data = cols[0].text.strip()
        title = cols[1].text.strip()

        # Skip rows without time data
        if ':' not in time_data:
            continue

        # Try block to safely handle errors or missing data
        try:
            full_time = datetime.strptime(today_str + " " + time_data, "%b-%d-%y %I:%M%p")
        except Exception as e:
            # Handle parse failure without crashing
            continue

        articles.append({
            'title': title,
            'publishedAt': full_time.strftime("%Y-%m-%d %H:%M")
        })

    # Return the final processed result
    return articles



