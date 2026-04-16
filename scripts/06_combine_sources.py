import pandas as pd

REVIEWS_PATH = "data/processed/reviews_bert.csv"
SOCIAL_PATH = "data/processed/social_posts_bert.csv"
OUTPUT_PATH = "data/processed/combined_sentiment.csv"
KEEP_COLS = ["review_text", "bert_label", "bert_score", "source"]


def main():
    df_reviews = pd.read_csv(REVIEWS_PATH).rename(columns={"Text": "review_text"})
    df_reviews["source"] = "reviews"
    df_reviews["bert_label"] = df_reviews["bert_label"].str.lower()

    df_social = pd.read_csv(SOCIAL_PATH)
    df_social["bert_label"] = df_social["bert_label"].str.lower()

    missing_reviews = [column for column in KEEP_COLS if column not in df_reviews.columns]
    missing_social = [column for column in KEEP_COLS if column not in df_social.columns]
    if missing_reviews:
        raise KeyError(f"Reviews data is missing columns: {missing_reviews}")
    if missing_social:
        raise KeyError(f"Social data is missing columns: {missing_social}")

    df_combined = pd.concat(
        [df_reviews[KEEP_COLS], df_social[KEEP_COLS]],
        ignore_index=True,
    )

    if df_combined["review_text"].isna().any():
        raise ValueError("Combined dataset still contains missing review_text values")

    df_combined.to_csv(OUTPUT_PATH, index=False)

    print(f"Total rows: {len(df_combined)}")
    print(df_combined.groupby(["source", "bert_label"]).size())
    print(f"\nSaved combined dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
