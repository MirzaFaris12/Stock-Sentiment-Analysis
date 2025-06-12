import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news_finviz(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    news_table = soup.find('table', class_='fullview-news-outer')
    if news_table is None:
        return []

    rows = news_table.find_all('tr')
    articles = []

    today_str = datetime.now().strftime("%b-%d-%y")  # e.g., Jun-11-25

    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue
        time_data = cols[0].text.strip()
        title = cols[1].text.strip()

        # Skip non-timestamp rows
        if ':' not in time_data:
            continue

        try:
            full_time = datetime.strptime(today_str + " " + time_data, "%b-%d-%y %I:%M%p")
        except Exception as e:
            continue

        articles.append({
            'title': title,
            'publishedAt': full_time.strftime("%Y-%m-%d %H:%M")
        })

    return articles



