import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIG ---
RAW_PATH = "data/raw/reviews.csv"
OUTPUT_PATH = "data/processed/reviews_vader.csv"
SAMPLE_SIZE = 5000

# --- LOAD ---
df = pd.read_csv(RAW_PATH, nrows=SAMPLE_SIZE)

# --- VADER SETUP ---
analyzer = SentimentIntensityAnalyzer()

# --- APPLY SENTIMENT ---
def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    compound = score["compound"]
    if compound >= 0.05:
        return compound, "positive"
    elif compound <= -0.05:
        return compound, "negative"
    else:
        return compound, "neutral"

df[["compound_score", "sentiment_label"]] = df["Text"].apply(
    lambda x: pd.Series(get_sentiment(x))
)

# --- INSPECT RESULTS ---
print("=" * 40)
print("SENTIMENT DISTRIBUTION:")
print(df["sentiment_label"].value_counts())

print("\nSCORE vs SENTIMENT (sample):")
print(df[["Score", "compound_score", "sentiment_label"]].head(10))

print("\nAVERAGE COMPOUND SCORE BY STAR RATING:")
print(df.groupby("Score")["compound_score"].mean().round(3))

# --- EXPORT ---
df.to_csv(OUTPUT_PATH, index=False)
print(f"\nExported to {OUTPUT_PATH}")