import pandas as pd
import argparse
import os
import requests
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer


def get_top_themes(df, label_col, label_val, text_col, n=5):
    subset = df[df[label_col] == label_val][text_col].dropna()
    if len(subset) == 0:
        return []
    tfidf = TfidfVectorizer(max_features=20, stop_words='english')
    tfidf.fit(subset)
    scores = zip(tfidf.get_feature_names_out(), tfidf.idf_)
    sorted_scores = sorted(scores, key=lambda x: x[1])
    return [word for word, _ in sorted_scores[:n]]


def generate_ai_summary(stats: dict) -> str:
    prompt = f"""You are a marketing analyst. Write a 3-paragraph executive summary based on these sentiment stats:
- Total Reviews: {stats['total']}
- Positive: {stats['positive_pct']}%
- Negative: {stats['negative_pct']}%
- Top negative themes: {stats['negative_themes']}
- Top positive themes: {stats['positive_themes']}

Cover: sentiment health, business concerns, and 2 actionable recommendations."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', default=datetime.today().strftime('%Y-%m-%d'))
    args = parser.parse_args()

    df = pd.read_csv("data/processed/reviews_bert.csv")

    total = len(df)
    positive = (df['bert_label'].str.upper() == 'POSITIVE').sum()
    negative = (df['bert_label'].str.upper() == 'NEGATIVE').sum()
    avg_confidence = df['bert_score'].mean()

    positive_pct = round(positive / total * 100, 1)
    negative_pct = round(negative / total * 100, 1)

    pos_themes = get_top_themes(df, 'bert_label', 'POSITIVE', 'Text')
    neg_themes = get_top_themes(df, 'bert_label', 'NEGATIVE', 'Text')

    report = f"""
============================================================
  SENTIMENT ANALYSIS REPORT - {args.date}
============================================================

OVERVIEW
----------------------------------------
Total Reviews Analysed : {total:,}
Avg BERT Confidence    : {avg_confidence:.4f}

SENTIMENT BREAKDOWN
----------------------------------------
  POSITIVE    : {positive:>5} reviews  ({positive_pct}%)
  NEGATIVE    : {negative:>5} reviews  ({negative_pct}%)

TOP 5 POSITIVE THEMES
----------------------------------------
{chr(10).join(f'  {i+1}. {t}' for i, t in enumerate(pos_themes))}

TOP 5 NEGATIVE THEMES
----------------------------------------
{chr(10).join(f'  {i+1}. {t}' for i, t in enumerate(neg_themes))}

============================================================
  AI EXECUTIVE SUMMARY
============================================================
"""

    print(report)

    stats = {
        'total': total,
        'positive_pct': positive_pct,
        'negative_pct': negative_pct,
        'positive_themes': pos_themes,
        'negative_themes': neg_themes
    }

    print("Generating AI summary via Ollama...")
    ai_summary = generate_ai_summary(stats)
    report += ai_summary
    report += "\n\n============================================================\n  END OF REPORT\n============================================================\n"

    print(ai_summary)
    print("\n============================================================")
    print("  END OF REPORT")
    print("============================================================")

    output_path = f"reports/sentiment_report_{args.date}.txt"
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()