import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news_finviz(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find("table", class_="fullview-news-outer")
    if news_table is None:
        return []

    rows = news_table.find_all("tr")
    news_list = []

    for row in rows:
        time_data = row.td.text.strip()
        headline = row.a.text.strip()
        link = row.a["href"]

        # Determine if time_data contains a date
        if "-" in time_data:  # Format: "May-29-25 03:25PM"
            date_obj = datetime.strptime(time_data, "%b-%d-%y %I:%M%p")
        else:  # Format: "03:25PM" - today
            today_str = datetime.today().strftime("%Y-%m-%d")
            date_obj = datetime.strptime(today_str + " " + time_data, "%Y-%m-%d %I:%M%p")

        news_list.append({
            "title": headline,
            "url": link,
            "publishedAt": date_obj.isoformat()  # ISO format: "YYYY-MM-DDTHH:MM:SS"
        })

    return news_list


