import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/processed/reviews_bert.csv")
negative_df = df[df["bert_label"] == "NEGATIVE"].copy()
print(f"Total negative reviews: {len(negative_df)}")

vectorizer = TfidfVectorizer(max_features=20, stop_words="english", ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(negative_df["Text"].fillna(""))

feature_names = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.sum(axis=0).A1

keywords_df = pd.DataFrame({"keyword": feature_names, "tfidf_score": tfidf_scores}).sort_values("tfidf_score", ascending=False).reset_index(drop=True)
keywords_df.to_csv("data/processed/negative_topics.csv", index=False)
print(keywords_df.to_string(index=False))
print("Saved to data/processed/negative_topics.csv")
