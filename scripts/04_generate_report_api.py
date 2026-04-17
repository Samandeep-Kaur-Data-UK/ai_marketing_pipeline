import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

from llm_utils import (
    LLMConfigurationError,
    LLMRequestError,
    available_provider,
    generate_text,
    provider_display_name,
)
from theme_utils import extract_top_themes


DEFAULT_INPUT_PATH = "data/processed/reviews_bert.csv"
DEFAULT_REPORT_TITLE = "SENTIMENT ANALYSIS REPORT"
TEXT_COLUMN_CANDIDATES = ("Text", "review_text", "text")


def infer_text_column(df: pd.DataFrame, requested_column: str | None) -> str:
    if requested_column:
        if requested_column not in df.columns:
            raise KeyError(f"Text column '{requested_column}' not found in input dataset.")
        return requested_column

    for column in TEXT_COLUMN_CANDIDATES:
        if column in df.columns:
            return column

    raise KeyError(
        f"Could not infer a text column. Tried: {', '.join(TEXT_COLUMN_CANDIDATES)}"
    )


def build_output_path(input_path: str, run_date: str, explicit_output: str | None) -> Path:
    if explicit_output:
        return Path(explicit_output)

    input_name = Path(input_path).stem
    if input_name == "combined_sentiment":
        return Path(f"reports/combined_sentiment_report_{run_date}.txt")

    return Path(f"reports/sentiment_report_{run_date}.txt")


def build_source_breakdown(df: pd.DataFrame) -> tuple[list[str], list[dict]]:
    if "source" not in df.columns:
        return [], []

    lines = []
    records = []
    for source, group in df.groupby("source"):
        total = len(group)
        positive = int((group["bert_label_norm"] == "POSITIVE").sum())
        negative = int((group["bert_label_norm"] == "NEGATIVE").sum())
        neutral = int((group["bert_label_norm"] == "NEUTRAL").sum())
        record = {
            "source": source,
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        }
        records.append(record)

        lines.append(
            f"  {source:<8} : total {total:>4} | "
            f"positive {positive:>4} ({positive / total * 100:>5.1f}%) | "
            f"negative {negative:>4} ({negative / total * 100:>5.1f}%)"
            + (
                f" | neutral {neutral:>4} ({neutral / total * 100:>5.1f}%)"
                if neutral
                else ""
            )
        )

    return lines, records


def build_local_summary(stats: dict) -> str:
    positive_themes = ", ".join(stats["positive_themes"]) or "product quality and convenience"
    negative_themes = ", ".join(stats["negative_themes"]) or "pricing and delivery issues"

    if stats["positive_pct"] >= 70:
        health_description = "strong"
    elif stats["positive_pct"] >= 60:
        health_description = "broadly positive"
    else:
        health_description = "mixed"

    source_note = ""
    if stats["source_records"]:
        most_negative_source = max(
            stats["source_records"],
            key=lambda record: (record["negative"] / record["total"], record["negative"]),
        )
        source_note = (
            f" Source comparison shows {most_negative_source['source']} is the most negative "
            f"channel in this dataset, so that source should be monitored first when sentiment weakens."
        )

    return (
        f"Customer sentiment is {health_description}, with {stats['positive_pct']}% of records "
        f"classified as positive versus {stats['negative_pct']}% negative across {stats['total']:,} "
        f"records. Positive language centres on {positive_themes}, which suggests customers mainly "
        f"value taste, product quality, and an overall dependable experience.\n\n"
        f"The main commercial risk sits in recurring negative themes such as {negative_themes}. "
        f"Those themes point to product-level friction that can weaken repeat purchase intent and "
        f"trust, especially when expectations on taste or quality are not consistently met.{source_note}\n\n"
        "Two practical actions stand out. First, prioritise the most frequent complaint themes for "
        "root-cause analysis with product and operations teams so quality issues can be fixed at source. "
        "Second, track negative theme shifts weekly and feed that trend into marketing and customer care "
        "so messaging and service responses can be adjusted before sentiment deteriorates further."
    )


def build_llm_user_prompt(stats: dict) -> str:
    source_lines = stats["source_breakdown_lines"] or ["  No source breakdown available"]

    return f"""Dataset name: {stats['dataset_name']}
Total records: {stats['total']}
Positive: {stats['positive']} ({stats['positive_pct']}%)
Negative: {stats['negative']} ({stats['negative_pct']}%)
Neutral: {stats['neutral']} ({stats['neutral_pct']}%)
Average BERT confidence: {stats['avg_confidence']}
Top positive themes: {stats['positive_themes']}
Top negative themes: {stats['negative_themes']}
Source breakdown:
{chr(10).join(source_lines)}

Write exactly 3 short paragraphs:
1. Overall sentiment health
2. Main business concern(s)
3. Exactly 2 actionable recommendations

Keep it concise, business-focused, and plain English."""


def generate_executive_summary(stats: dict) -> tuple[str, str]:
    provider = available_provider()
    if provider is None:
        return build_local_summary(stats), "local Python summary"

    system_prompt = (
        "You are a UK marketing data analyst writing a business-ready executive summary "
        "for a sentiment analysis pipeline."
    )

    try:
        summary = generate_text(
            system_prompt=system_prompt,
            user_prompt=build_llm_user_prompt(stats),
            max_tokens=700,
            temperature=0.4,
        )
        return summary.strip(), provider_display_name(provider)
    except (LLMConfigurationError, LLMRequestError, Exception) as exc:
        print(
            f"Claude/GPT narrative generation unavailable, using local Python summary instead: {exc}"
        )
        return build_local_summary(stats), "local Python summary"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.today().strftime("%Y-%m-%d"))
    parser.add_argument("--input", default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output")
    parser.add_argument("--text-column")
    parser.add_argument("--title", default=DEFAULT_REPORT_TITLE)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    text_column = infer_text_column(df, args.text_column)
    df["bert_label_norm"] = df["bert_label"].astype(str).str.upper()

    total = len(df)
    positive = int((df["bert_label_norm"] == "POSITIVE").sum())
    negative = int((df["bert_label_norm"] == "NEGATIVE").sum())
    neutral = int((df["bert_label_norm"] == "NEUTRAL").sum())
    avg_confidence = round(float(df["bert_score"].mean()), 4)

    positive_pct = round(positive / total * 100, 1)
    negative_pct = round(negative / total * 100, 1)
    neutral_pct = round(neutral / total * 100, 1)

    pos_themes = extract_top_themes(
        df,
        label_col="bert_label_norm",
        label_value="POSITIVE",
        text_col=text_column,
        n=5,
        min_df=3,
    )
    neg_themes = extract_top_themes(
        df,
        label_col="bert_label_norm",
        label_value="NEGATIVE",
        text_col=text_column,
        n=5,
        min_df=3,
    )
    source_breakdown_lines, source_records = build_source_breakdown(df)

    report = f"""
============================================================
  {args.title} - {args.date}
============================================================

DATASET
----------------------------------------
Input File              : {args.input}
Text Column             : {text_column}
Total Records Analysed  : {total:,}
Avg BERT Confidence     : {avg_confidence:.4f}

SENTIMENT BREAKDOWN
----------------------------------------
  POSITIVE    : {positive:>5} records  ({positive_pct}%)
  NEGATIVE    : {negative:>5} records  ({negative_pct}%)
  NEUTRAL     : {neutral:>5} records  ({neutral_pct}%)

TOP 5 POSITIVE THEMES
----------------------------------------
{chr(10).join(f'  {i + 1}. {theme}' for i, theme in enumerate(pos_themes))}

TOP 5 NEGATIVE THEMES
----------------------------------------
{chr(10).join(f'  {i + 1}. {theme}' for i, theme in enumerate(neg_themes))}
"""

    if source_breakdown_lines:
        report += f"""

SOURCE BREAKDOWN
----------------------------------------
{chr(10).join(source_breakdown_lines)}
"""

    report += """

============================================================
  EXECUTIVE SUMMARY
============================================================
"""

    print(report)

    stats = {
        "dataset_name": Path(args.input).name,
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "neutral_pct": neutral_pct,
        "avg_confidence": avg_confidence,
        "positive_themes": pos_themes,
        "negative_themes": neg_themes,
        "source_breakdown_lines": source_breakdown_lines,
        "source_records": source_records,
    }

    summary, summary_method = generate_executive_summary(stats)
    print(f"Generating executive summary via {summary_method}...")
    report += summary
    report += (
        "\n\n============================================================\n"
        "  END OF REPORT\n"
        "============================================================\n"
    )

    print(summary)
    print("\n============================================================")
    print("  END OF REPORT")
    print("============================================================")

    output_path = build_output_path(args.input, args.date, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
