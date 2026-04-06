import pandas as pd
from sklearn.metrics import classification_report

# --- LOAD ---
df = pd.read_csv("data/processed/reviews_bert.csv")

# --- MAP STAR RATINGS TO GROUND TRUTH ---
# 1-2 stars = NEGATIVE, 3 stars = skip (ambiguous), 4-5 stars = POSITIVE
df_filtered = df[df["Score"] != 3].copy()

df_filtered["ground_truth"] = df_filtered["Score"].apply(
    lambda x: "POSITIVE" if x >= 4 else "NEGATIVE"
)

# --- NORMALISE LABELS ---
df_filtered["vader_label_norm"] = df_filtered["sentiment_label"].str.upper()
df_filtered["bert_label_norm"]  = df_filtered["bert_label"].str.upper()

# --- VADER REPORT ---
print("=" * 40)
print("VADER ACCURACY REPORT")
print("=" * 40)
vader_report = classification_report(
    df_filtered["ground_truth"],
    df_filtered["vader_label_norm"],
    labels=["POSITIVE", "NEGATIVE"],
    output_dict=False
)
print(vader_report)

# --- BERT REPORT ---
print("=" * 40)
print("BERT ACCURACY REPORT")
print("=" * 40)
bert_report = classification_report(
    df_filtered["ground_truth"],
    df_filtered["bert_label_norm"],
    labels=["POSITIVE", "NEGATIVE"],
    output_dict=False
)
print(bert_report)

# --- SAVE RESULTS ---
vader_dict = classification_report(
    df_filtered["ground_truth"],
    df_filtered["vader_label_norm"],
    labels=["POSITIVE", "NEGATIVE"],
    output_dict=True
)
bert_dict = classification_report(
    df_filtered["ground_truth"],
    df_filtered["bert_label_norm"],
    labels=["POSITIVE", "NEGATIVE"],
    output_dict=True
)

summary = pd.DataFrame({
    "Model": ["VADER", "BERT"],
    "Accuracy": [
        round(vader_dict["weighted avg"]["recall"], 3),
        round(bert_dict["weighted avg"]["recall"], 3)
    ],
    "Positive_F1": [
        round(vader_dict["POSITIVE"]["f1-score"], 3),
        round(bert_dict["POSITIVE"]["f1-score"], 3)
    ],
    "Negative_F1": [
        round(vader_dict["NEGATIVE"]["f1-score"], 3),
        round(bert_dict["NEGATIVE"]["f1-score"], 3)
    ]
})

summary.to_csv("data/processed/model_comparison.csv", index=False)
print("\nModel comparison summary:")
print(summary)
print("\nSaved to data/processed/model_comparison.csv")