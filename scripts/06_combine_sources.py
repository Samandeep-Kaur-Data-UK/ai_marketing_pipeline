import pandas as pd

df_reviews = pd.read_csv("data/processed/reviews_bert.csv")
df_reviews["source"] = "reviews"
df_reviews["bert_label"] = df_reviews["bert_label"].str.lower()  # fix casing

df_social = pd.read_csv("data/processed/social_posts_bert.csv")

keep_cols = ["review_text", "bert_label", "bert_score", "source"]

df_reviews = df_reviews[[c for c in keep_cols if c in df_reviews.columns]]
df_social = df_social[[c for c in keep_cols if c in df_social.columns]]

df_combined = pd.concat([df_reviews, df_social], ignore_index=True)

df_combined.to_csv("data/processed/combined_sentiment.csv", index=False)

print(f"Total rows: {len(df_combined)}")
print(df_combined.groupby(["source", "bert_label"]).size())