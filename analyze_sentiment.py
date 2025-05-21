from transformers import pipeline

# Load FinBERT sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def score_articles(articles):
    results = []
    for article in articles:
        title = article.get("title", "")
        if not title:
            continue

        # Run FinBERT sentiment prediction
        output = sentiment_model(title)[0]
        label = output["label"]
        confidence = output["score"]

        # Convert FinBERT labels to sentiment scores
        if label == "positive":
            sentiment = confidence
        elif label == "negative":
            sentiment = -confidence
        else:
            sentiment = 0.0  # neutral

        results.append({
            "title": title,
            "sentiment": sentiment,
            "confidence": confidence,
            "publishedAt": article.get("publishedAt")  # ✅ Preserve the timestamp
        })

    return results

