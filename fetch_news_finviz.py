import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_finviz_date(date_str):
    """
    Attempt to parse the Finviz date string using multiple known formats.
    Returns a datetime object if successful, otherwise None.
    """
    for fmt in ("%b-%d-%y %I:%M%p", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def fetch_news_finviz(ticker):
    """
    Fetch news headlines for the given ticker from Finviz.
    Returns a list of articles with 'title', 'url', and 'publishedAt'.
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_table = soup.find("table", class_="fullview-news-outer")
    if not news_table:
        print("⚠️ No news table found.")
        return []

    rows = news_table.find_all("tr")
    articles = []

    for row in rows:
        title_elem = row.find_all("td")[1].a
        if title_elem:
            title = title_elem.text.strip()
            link = title_elem.get("href")

            # Extract timestamp
            time_data = row.td.text.strip()
            today_str = datetime.now().strftime("%Y-%m-%d")
            if ":" in time_data:
                # Only time is provided; combine with today’s date
                date_str = f"{today_str} {time_data}"
            else:
                # Full date provided (like 'May-30-25 01:23PM')
                date_str = time_data

            # Parse the date
            published_at = parse_finviz_date(date_str)
            if published_at:
                published_at_str = published_at.isoformat()
            else:
                published_at_str = None  # Handle later in app if needed

            articles.append({
                "title": title,
                "url": link,
                "publishedAt": published_at_str
            })

    return articles



