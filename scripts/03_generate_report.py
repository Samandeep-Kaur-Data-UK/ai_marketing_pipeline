import pandas as pd
import argparse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS


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


def generate_executive_summary(stats: dict) -> str:
    positive_themes = ", ".join(stats["positive_themes"]) or "product quality and convenience"
    negative_themes = ", ".join(stats["negative_themes"]) or "pricing and delivery issues"

    if stats["positive_pct"] >= 70:
        health_description = "strong"
    elif stats["positive_pct"] >= 60:
        health_description = "broadly positive"
    else:
        health_description = "mixed"

    return (
        f"Customer sentiment is {health_description}, with {stats['positive_pct']}% of reviews "
        f"classified as positive versus {stats['negative_pct']}% negative across {stats['total']:,} "
        f"reviews. Positive language centres on {positive_themes}, which suggests customers mainly "
        f"value taste, product quality, and an overall dependable experience.\n\n"
        f"The main commercial risk sits in recurring negative themes such as {negative_themes}. "
        f"Those themes point to product-level friction that can weaken repeat purchase intent and "
        f"trust, especially when customers feel expectations on taste or quality are not consistently met.\n\n"
        "Two practical actions stand out. First, prioritise the most frequent complaint themes for "
        "root-cause analysis with product and operations teams so quality issues can be fixed at source. "
        "Second, track the negative theme mix weekly and feed that trend into marketing and customer care "
        "so messaging and service responses can be adjusted before sentiment deteriorates further."
    )


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
  EXECUTIVE SUMMARY
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

    print("Generating executive summary in Python...")
    executive_summary = generate_executive_summary(stats)
    report += executive_summary
    report += "\n\n============================================================\n  END OF REPORT\n============================================================\n"

    print(executive_summary)
    print("\n============================================================")
    print("  END OF REPORT")
    print("============================================================")

    output_path = f"reports/sentiment_report_{args.date}.txt"
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
