import pandas as pd
from transformers import pipeline

df = pd.read_csv("data/processed/social_posts_raw.csv")
print(f"Loaded {len(df)} social posts.")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    max_length=512
)

results = sentiment_pipeline(df["review_text"].tolist(), batch_size=32)

df["bert_label"] = [r["label"].lower() for r in results]
df["bert_score"] = [round(r["score"], 4) for r in results]

df.to_csv("data/processed/social_posts_bert.csv", index=False)
print(df["bert_label"].value_counts())
print(df.head(3))