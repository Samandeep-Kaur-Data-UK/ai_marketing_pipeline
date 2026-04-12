import pandas as pd
import argparse
from pathlib import Path
from collections import Counter
import re
from datetime import date
import ollama

def extract_themes(texts: pd.Series, top_n: int = 5) -> list[tuple[str, int]]:
    """Extract top N keyword themes from review text."""
    stopwords = {
        "the","and","is","it","this","a","to","of","i","was","for",
        "in","my","that","have","not","but","with","on","so","they",
        "be","are","has","an","at","from","or","we","as","very","just",
        "its","if","can","all","do","get","had","he","she","you","your",
        "these","them","like","their","there","been","more","also","what",
        "would","could","when","than","then","some","out","about","will",
        "one","up","no","which","were","our","who","after","only","other",
        "really","even","made","make","still","came","into","over","time",
        "use","used","much","too","good","well","back","got","way","did"
    }
    words = []
    for text in texts.dropna():
        tokens = re.findall(r'\b[a-z]{4,}\b', text.lower())
        words.extend([t for t in tokens if t not in stopwords])
    return Counter(words).most_common(top_n)


def generate_report(input_path: str, report_date: str) -> None:
    df = pd.read_csv(input_path)

    total = len(df)
    sentiment_counts = df['bert_label'].value_counts()
    sentiment_pct = (sentiment_counts / total * 100).round(1)
    avg_confidence = df['bert_score'].mean()
    agreement_rate = df['agreement'].mean()

    positive_reviews = df[df['bert_label'] == 'POSITIVE']['Text']
    negative_reviews = df[df['bert_label'] == 'NEGATIVE']['Text']

    top_positive = extract_themes(positive_reviews)
    top_negative = extract_themes(negative_reviews)

    lines = [
        "=" * 60,
        f"  SENTIMENT ANALYSIS REPORT - {report_date}",
        "=" * 60,
        "",
        "OVERVIEW",
        "-" * 40,
        f"Total Reviews Analysed : {total:,}",
        f"Avg BERT Confidence    : {avg_confidence:.4f}",
        f"VADER/BERT Agreement   : {agreement_rate:.1%}",
        "",
        "SENTIMENT BREAKDOWN",
        "-" * 40,
    ]
    for label, pct in sentiment_pct.items():
        count = sentiment_counts[label]
        lines.append(f"  {label:<12}: {count:>5} reviews  ({pct}%)")

    lines += [
        "",
        "TOP 5 POSITIVE THEMES",
        "-" * 40,
    ]
    for i, (word, freq) in enumerate(top_positive, 1):
        lines.append(f"  {i}. {word:<20} (mentioned {freq} times)")

    lines += [
        "",
        "TOP 5 NEGATIVE THEMES",
        "-" * 40,
    ]
    for i, (word, freq) in enumerate(top_negative, 1):
        lines.append(f"  {i}. {word:<20} (mentioned {freq} times)")

    # --- AI Narrative ---
    prompt = f"""You are a senior marketing analyst writing for a non-technical stakeholder.

Sentiment results:
- Total reviews: {total:,}
- Positive: {sentiment_pct.get('POSITIVE', 0)}%
- Negative: {sentiment_pct.get('NEGATIVE', 0)}%
- Neutral: {sentiment_pct.get('NEUTRAL', 0)}%
- Avg confidence: {avg_confidence:.2f}
- Top negative themes: {', '.join([w for w, _ in top_negative])}
- Top positive themes: {', '.join([w for w, _ in top_positive])}

Write exactly 3 paragraphs:
1. Overall sentiment health and what it signals.
2. Key concerns from negative themes and business implications.
3. Two specific actionable recommendations for the marketing team.

Plain business English. No bullet points."""

    response = ollama.chat('llama3.2', messages=[{'role': 'user', 'content': prompt}])
    narrative = response['message']['content']

    lines += [
        "",
        "=" * 60,
        "  AI EXECUTIVE SUMMARY",
        "=" * 60,
        "",
        narrative,
        "",
        "=" * 60,
        "  END OF REPORT",
        "=" * 60,
    ]

    report_text = "\n".join(lines)

    output_path = Path("reports") / f"sentiment_report_{report_date}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text)

    print(report_text)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Sentiment Report")
    parser.add_argument("--date", type=str, default=str(date.today()),
                        help="Report date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--input", type=str, default="data/processed/reviews_bert.csv",
                        help="Path to reviews_bert.csv")
    args = parser.parse_args()

    generate_report(args.input, args.date)