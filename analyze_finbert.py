from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Load FinBERT model + tokenizer
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

labels = ['Negative', 'Neutral', 'Positive']

def score_with_finbert(texts):
    results = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1).numpy()[0]
        sentiment = labels[np.argmax(probs)]
        results.append({
            "title": text,
            "sentiment": sentiment,
            "confidence": float(np.max(probs))
        })
    return results

