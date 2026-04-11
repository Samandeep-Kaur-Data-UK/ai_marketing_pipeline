from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = "data/processed/reviews_bert.csv"
OUTPUT_PATH = "reports/sentiment_trend.png"


df = pd.read_csv(INPUT_PATH)

# Day 52 tracker requirement: parse timestamps and chart monthly average bert_score.
df["review_date"] = pd.to_datetime(df["Time"], unit="s")
df["review_month"] = df["review_date"].dt.to_period("M")

monthly = (
    df.groupby("review_month")
    .agg(
        avg_bert_score=("bert_score", "mean"),
        review_count=("bert_score", "count"),
    )
    .reset_index()
)
monthly["review_month_str"] = monthly["review_month"].astype(str)

overall_avg_score = monthly["avg_bert_score"].mean()

plt.figure(figsize=(14, 6))
plt.plot(
    monthly["review_month_str"],
    monthly["avg_bert_score"],
    color="#16538C",
    linewidth=2.5,
    marker="o",
    markersize=4,
    label="Monthly Avg BERT Score",
)
plt.axhline(
    y=overall_avg_score,
    color="#E76F2E",
    linestyle="--",
    linewidth=1.8,
    label=f"Overall Avg: {overall_avg_score:.3f}",
)

step = max(1, len(monthly) // 12)
tick_positions = list(range(0, len(monthly), step))
plt.xticks(
    tick_positions,
    monthly["review_month_str"].iloc[::step],
    rotation=45,
    ha="right",
    fontsize=8,
)
plt.ylim(0.80, 1.01)
plt.ylabel("Average BERT Score", fontsize=11)
plt.xlabel("Month", fontsize=11)
plt.title(
    "Monthly Average BERT Sentiment Score - Amazon Fine Food Reviews",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.grid(axis="y", linestyle="--", alpha=0.25)
plt.legend()
plt.tight_layout()

output_path = Path(OUTPUT_PATH)
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close()

print(f"Chart saved to: {output_path}")
print(f"Months included: {len(monthly)}")
print(
    f"Date range: {monthly['review_month_str'].iloc[0]} to "
    f"{monthly['review_month_str'].iloc[-1]}"
)
print(f"Average monthly BERT score: {overall_avg_score:.3f}")
print(
    f"Lowest month: {monthly.loc[monthly['avg_bert_score'].idxmin(), 'review_month_str']} "
    f"({monthly['avg_bert_score'].min():.3f})"
)
print(
    f"Highest month: {monthly.loc[monthly['avg_bert_score'].idxmax(), 'review_month_str']} "
    f"({monthly['avg_bert_score'].max():.3f})"
)
