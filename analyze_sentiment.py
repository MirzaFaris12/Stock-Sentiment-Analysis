from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def score_articles(articles):
    analyzer = SentimentIntensityAnalyzer()
    results = []
    for a in articles:
        score = analyzer.polarity_scores(a.get('title', ''))
        results.append({
            "title": a.get('title', ''),
            "sentiment": score['compound']
        })
    return results
