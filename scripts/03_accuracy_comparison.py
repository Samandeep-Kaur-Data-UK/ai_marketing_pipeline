from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


INPUT_PATH = Path("data/processed/reviews_bert.csv")
SUMMARY_OUTPUT_PATH = Path("data/processed/model_comparison.csv")
NOTES_OUTPUT_PATH = Path("project_notes.md")


def load_comparison_frame() -> pd.DataFrame:
    df = pd.read_csv(INPUT_PATH)

    # Map review scores to a binary ground truth and drop 3-star reviews,
    # which are too ambiguous for a clean positive/negative comparison.
    df = df[df["Score"] != 3].copy()
    df["ground_truth"] = df["Score"].apply(
        lambda score: "POSITIVE" if score >= 4 else "NEGATIVE"
    )
    df["vader_label_norm"] = df["sentiment_label"].astype(str).str.upper()
    df["bert_label_norm"] = df["bert_label"].astype(str).str.upper()
    return df


def build_report_dict(df: pd.DataFrame, prediction_column: str) -> dict:
    return classification_report(
        df["ground_truth"],
        df[prediction_column],
        labels=["POSITIVE", "NEGATIVE"],
        output_dict=True,
    )


def print_console_report(title: str, df: pd.DataFrame, prediction_column: str) -> None:
    print("=" * 40)
    print(title)
    print("=" * 40)
    print(
        classification_report(
            df["ground_truth"],
            df[prediction_column],
            labels=["POSITIVE", "NEGATIVE"],
            output_dict=False,
        )
    )


def build_summary_frame(
    vader_dict: dict,
    bert_dict: dict,
    vader_accuracy: float,
    bert_accuracy: float,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Model": ["VADER", "BERT"],
            "Accuracy": [
                round(vader_accuracy, 3),
                round(bert_accuracy, 3),
            ],
            "Positive_F1": [
                round(vader_dict["POSITIVE"]["f1-score"], 3),
                round(bert_dict["POSITIVE"]["f1-score"], 3),
            ],
            "Negative_F1": [
                round(vader_dict["NEGATIVE"]["f1-score"], 3),
                round(bert_dict["NEGATIVE"]["f1-score"], 3),
            ],
        }
    )


def write_project_notes(
    vader_dict: dict,
    bert_dict: dict,
    vader_accuracy: float,
    bert_accuracy: float,
) -> None:
    notes = f"""# Project 2 Notes

## Day 49 - Accuracy Comparison: VADER vs BERT

Ground truth mapping:
- 1-2 stars = NEGATIVE
- 3 stars = excluded as ambiguous
- 4-5 stars = POSITIVE

### Headline Results

| Model | Accuracy | Positive F1 | Negative F1 |
| --- | ---: | ---: | ---: |
| VADER | {vader_accuracy:.3f} | {vader_dict['POSITIVE']['f1-score']:.3f} | {vader_dict['NEGATIVE']['f1-score']:.3f} |
| BERT | {bert_accuracy:.3f} | {bert_dict['POSITIVE']['f1-score']:.3f} | {bert_dict['NEGATIVE']['f1-score']:.3f} |

### Precision and Recall by Class

#### VADER
- POSITIVE precision: {vader_dict['POSITIVE']['precision']:.3f}
- POSITIVE recall: {vader_dict['POSITIVE']['recall']:.3f}
- NEGATIVE precision: {vader_dict['NEGATIVE']['precision']:.3f}
- NEGATIVE recall: {vader_dict['NEGATIVE']['recall']:.3f}

#### BERT
- POSITIVE precision: {bert_dict['POSITIVE']['precision']:.3f}
- POSITIVE recall: {bert_dict['POSITIVE']['recall']:.3f}
- NEGATIVE precision: {bert_dict['NEGATIVE']['precision']:.3f}
- NEGATIVE recall: {bert_dict['NEGATIVE']['recall']:.3f}

### Interpretation

VADER achieves slightly higher overall accuracy, but BERT is materially better at detecting negative sentiment.
For marketing analytics, the cost of missing negative feedback is higher than the benefit of a small accuracy edge,
so BERT remains the better production choice for this project.

## Final Retrospective

### What went well
- The repo now runs as a clear pipeline from raw CSV to dashboard-ready outputs rather than a collection of isolated exercises.
- DistilBERT produced the most commercially useful signal because it captured negative sentiment far better than the VADER baseline.
- Extending the project with synthetic social data made the final dashboard more realistic by introducing source-level comparison.
- The finished portfolio package includes documentation, reports, visuals, and a Power BI asset so reviewers can assess both technical work and communication.

### What was challenging
- Hosted LLM access was inconsistent during development, so the reporting workflow had to support both API-based and deterministic local summaries.
- Early path and column mismatches across scripts created avoidable rework and showed the value of stricter project conventions.
- The lighter final architecture was chosen deliberately after heavier local model-serving options proved unreliable on available hardware.

### What I would improve next
- Centralise file paths and runtime settings in a small configuration module to reduce duplication across scripts.
- Add lightweight automated tests for schema checks and output validation so regressions surface earlier.
- Evaluate domain-specific fine-tuning or calibration to improve negative precision for food and grocery feedback.
- Package the workflow for scheduled execution with logging so it can move from portfolio project to a repeatable reporting job.
"""

    NOTES_OUTPUT_PATH.write_text(notes)


def main() -> None:
    df = load_comparison_frame()

    print_console_report("VADER ACCURACY REPORT", df, "vader_label_norm")
    print_console_report("BERT ACCURACY REPORT", df, "bert_label_norm")

    vader_dict = build_report_dict(df, "vader_label_norm")
    bert_dict = build_report_dict(df, "bert_label_norm")
    vader_accuracy = accuracy_score(df["ground_truth"], df["vader_label_norm"])
    bert_accuracy = accuracy_score(df["ground_truth"], df["bert_label_norm"])
    summary = build_summary_frame(vader_dict, bert_dict, vader_accuracy, bert_accuracy)

    summary.to_csv(SUMMARY_OUTPUT_PATH, index=False)
    write_project_notes(vader_dict, bert_dict, vader_accuracy, bert_accuracy)

    print("Model comparison summary:")
    print(summary.to_string(index=False))
    print(f"\nSaved to {SUMMARY_OUTPUT_PATH}")
    print(f"Saved to {NOTES_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
