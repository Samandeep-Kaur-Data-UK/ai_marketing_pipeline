import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# --- LOAD ---
df = pd.read_csv("data/processed/reviews_bert.csv")

# --- FILTER TO NEGATIVE REVIEWS (BERT label) ---
negative_df = df[df["bert_label"] == "NEGATIVE"].copy()
print(f"Total negative reviews: {len(negative_df)}")

# --- TF-IDF ON NEGATIVE REVIEW TEXT ---
vectorizer = TfidfVectorizer(
    max_features=20,
    stop_words="english",
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(negative_df["Text"].fillna(""))

# --- EXTRACT TOP KEYWORDS ---
feature_names = vectorizer.get_feature_names_out()
tfidf_scores  = tfidf_matrix.sum(axis=0).A1

keywords_df = pd.DataFrame({
    "keyword": feature_names,
    "tfidf_score": tfidf_scores
}).sort_values("tfidf_score", ascending=False).reset_index(drop=True)

# --- SAVE ---
keywords_df.to_csv("data/processed/negative_topics.csv", index=False)

# --- PRINT ---
print("\nTop 20 keywords from negative reviews:")
print("=" * 40)
print(keywords_df.to_string(index=False))
print("\nSaved to data/processed/negative_topics.csv")