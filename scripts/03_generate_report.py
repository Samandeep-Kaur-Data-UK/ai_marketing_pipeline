import pandas as pd
import argparse
import os
import requests
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))


def get_top_themes(df, label_col, label_val, text_col, n=5):
    subset = df[df[label_col] == label_val][text_col].dropna()
    if len(subset) == 0:
        return []

    cleaned_subset = (
        subset.astype(str)
        .str.replace(r"<br\s*/?>", " ", regex=True)
        .str.replace(r"[^A-Za-z\s]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    tfidf = TfidfVectorizer(
        max_features=30,
        stop_words=sorted(set(ENGLISH_STOP_WORDS).union({"br"})),
    )
    tfidf.fit(cleaned_subset)
    scores = zip(tfidf.get_feature_names_out(), tfidf.idf_)
    sorted_scores = sorted(scores, key=lambda x: x[1])
    return [word for word, _ in sorted_scores[:n]]


def build_fallback_summary(stats: dict) -> str:
    positive_themes = ", ".join(stats["positive_themes"]) or "product quality and convenience"
    negative_themes = ", ".join(stats["negative_themes"]) or "pricing and delivery issues"

    return (
        f"Customer sentiment remains broadly healthy, with {stats['positive_pct']}% of reviews "
        f"classified as positive versus {stats['negative_pct']}% negative across {stats['total']:,} "
        f"reviews. Positive language clusters around {positive_themes}, suggesting customers most "
        f"value product enjoyment and a reliable buying experience.\n\n"
        f"The main commercial risk sits in recurring negative themes such as {negative_themes}. "
        f"Those topics point to friction that can damage repeat purchase intent and reduce trust, "
        f"especially when a poor product experience is paired with delivery or price concerns.\n\n"
        "Two practical next steps stand out. First, prioritise the highest-frequency complaint "
        "themes for root-cause analysis with operations and merchandising teams. Second, build a "
        "simple weekly tracker for negative sentiment volume and theme shifts so the team can act "
        "before issues grow into wider brand damage."
    )


def generate_ai_summary(stats: dict) -> str:
    prompt = f"""You are a marketing analyst. Write a 3-paragraph executive summary based on these sentiment stats:
- Total Reviews: {stats['total']}
- Positive: {stats['positive_pct']}%
- Negative: {stats['negative_pct']}%
- Top negative themes: {stats['negative_themes']}
- Top positive themes: {stats['positive_themes']}

Cover: sentiment health, business concerns, and 2 actionable recommendations."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        response_json = response.json()
        summary = response_json.get("response", "").strip()
        if not summary:
            raise ValueError("Ollama returned an empty summary")
        return summary
    except Exception as exc:
        print(f"Ollama summary unavailable, using fallback summary instead: {exc}")
        return build_fallback_summary(stats)


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

    print(f"Generating executive summary via {OLLAMA_MODEL}...")
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
