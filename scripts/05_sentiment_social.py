import pandas as pd
from transformers import pipeline

INPUT_PATH = "data/processed/social_posts_raw.csv"
OUTPUT_PATH = "data/processed/social_posts_bert.csv"
BATCH_SIZE = 32


def main():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} social posts from {INPUT_PATH}.")

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
        max_length=512,
    )

    results = sentiment_pipeline(df["review_text"].fillna("").tolist(), batch_size=BATCH_SIZE)

    df["bert_label"] = [result["label"].lower() for result in results]
    df["bert_score"] = [round(result["score"], 4) for result in results]

    df.to_csv(OUTPUT_PATH, index=False)

    print("\nBERT label distribution:")
    print(df["bert_label"].value_counts())
    print(f"\nSaved labelled social posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
