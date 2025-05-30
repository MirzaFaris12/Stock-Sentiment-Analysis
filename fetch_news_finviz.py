import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news_finviz(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find("table", class_="fullview-news-outer")

    if not news_table:
        print("No news table found on the page.")
        return []

    articles = []
    for row in news_table.find_all("tr"):
        time_data = row.td.text.strip()
        headline = row.a.text.strip()
        link = "https://finviz.com" + row.a["href"]

        # Determine if time_data is just time (today) or full date (past)
        if len(time_data) == 5:  # e.g., '09:25'
            date_str = datetime.today().strftime("%Y-%m-%d") + " " + time_data
        else:  # e.g., 'May-21-24 09:25AM'
            date_str = datetime.strptime(time_data, "%b-%d-%y %I:%M%p").strftime("%Y-%m-%d %H:%M")

        articles.append({
            "title": headline,
            "publishedAt": date_str,
            "url": link
        })

    return articles

