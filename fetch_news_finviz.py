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

        
        # Check whether time_data contains only time (e.g., "03:25PM") or full date
        if "-" in time_data:  # Full date like "May-29-25 03:25PM"
            date_obj = datetime.strptime(time_data, "%b-%d-%y %I:%M%p")
        else:  # Only time, today
            today_str = datetime.today().strftime("%Y-%m-%d")
            date_obj = datetime.strptime(today_str + " " + time_data, "%Y-%m-%d %I:%M%p")

        # Convert to desired format if needed
        date_str = date_obj.strftime("%Y-%m-%d %H:%M")

        articles.append({
            "title": headline,
            "publishedAt": date_str,
            "url": link
        })

    return articles

