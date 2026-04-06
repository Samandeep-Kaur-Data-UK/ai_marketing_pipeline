import pandas as pd
from transformers import pipeline

# --- CONFIG ---
INPUT_PATH  = "data/processed/reviews_vader.csv"
OUTPUT_PATH = "data/processed/reviews_bert.csv"
SAMPLE_SIZE = 1000
BATCH_SIZE  = 32

# --- LOAD ---
df = pd.read_csv(INPUT_PATH)
sample = df.head(SAMPLE_SIZE).copy().reset_index(drop=True)

# --- LOAD BERT PIPELINE ---
print("Loading DistilBERT model...")
bert_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    max_length=512
)

# --- BATCH PROCESS ---
print(f"Running BERT on {SAMPLE_SIZE} reviews...")
texts = sample["Text"].fillna("").tolist()
results = bert_pipeline(texts, batch_size=BATCH_SIZE)

# --- ATTACH RESULTS ---
sample["bert_label"] = [r["label"] for r in results]
sample["bert_score"] = [round(r["score"], 4) for r in results]

# --- VADER vs BERT AGREEMENT ---
sample["agreement"] = (
    sample["sentiment_label"].str.upper() == sample["bert_label"].str.upper()
)
agreement_rate = sample["agreement"].mean() * 100

# --- SAVE ---
sample.to_csv(OUTPUT_PATH, index=False)

# --- SUMMARY ---
print("\n" + "=" * 40)
print("BERT label distribution:")
print(sample["bert_label"].value_counts())
print(f"\nVADER vs BERT agreement rate: {agreement_rate:.1f}%")
print("=" * 40)
print(f"\nSaved to {OUTPUT_PATH}")