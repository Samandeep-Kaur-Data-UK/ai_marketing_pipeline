# AI Marketing Pipeline
**Tech Stack:** Python, Pandas, VADER, DistilBERT, Scikit-learn, Power BI

Portfolio-ready sentiment analysis pipeline that turns customer text into a marketing reporting workflow. The project ingests Amazon review data, benchmarks VADER against DistilBERT, extracts complaint themes, generates business-facing summaries, and prepares outputs for Power BI.

## Portfolio Snapshot

- Problem: marketing teams cannot manually review thousands of comments and product reviews every week
- Data: 5,000 Amazon Fine Food reviews plus 500 synthetic FreshBasket UK social posts for cross-channel comparison
- Modelling decision: DistilBERT was selected over VADER because it captures negative sentiment more reliably
- Delivery: processed datasets, dated text reports, a trend chart, and a Power BI dashboard

## Business Problem

Marketing teams need a repeatable way to answer four questions quickly:

- Are customers broadly positive or negative right now?
- What themes are driving complaints?
- Which model is reliable enough for production monitoring?
- How does sentiment compare across channels such as reviews and social?

## Solution Summary

This repo automates that workflow with Python and Power BI:

- loads 5,000 Amazon Fine Food reviews for the project dataset
- scores sentiment with VADER and DistilBERT
- validates both models against review star ratings
- chooses the production model based on business impact, not just headline accuracy
- extracts the most common positive and negative themes
- generates dated text reports and a trend chart
- adds 500 synthetic FreshBasket UK social posts to simulate a second customer-feedback source
- combines both sources into one Power BI-ready dataset

## Why BERT Won

The key modelling question in this project is not "which model is most accurate overall?" but "which model is safer for a marketing team that cannot afford to miss unhappy customers?"

| Model | Accuracy | Positive F1 | Negative F1 |
| --- | ---: | ---: | ---: |
| VADER | 86.4% | 0.926 | 0.531 |
| DistilBERT | 85.0% | 0.904 | 0.652 |

VADER edges overall accuracy, but DistilBERT is materially better at detecting negative sentiment. That trade-off matters more for brand monitoring, so DistilBERT is the production model used in the reporting and dashboard outputs.

## Multi-Source Architecture

Mid-project, the social-data workflow moved away from a heavier local model-hosting setup because it was not practical on the available hardware. The final repo keeps the pipeline lighter and more professional:

- Day 56 report generation is Claude/GPT API-ready, with a deterministic local fallback
- Day 57 synthetic social data is generated through a documented prompt workflow with an API option and a local template fallback
- the final combined dataset keeps a `source` column so sentiment can be compared across reviews and social posts

```text
Amazon Reviews (CSV)
    -> 01_load_data.py
    -> 02_vader_sentiment.py
    -> 02_transformer_sentiment.py
    -> 03_accuracy_comparison.py
    -> 04_topic_extraction.py
    -> 04_generate_report_api.py
    -> 05_sentiment_trend.py
    -> Power BI

FreshBasket UK Social Posts
    -> 04_generate_social_posts.py
    -> 05_score_social.py
    -> 06_combine_sources.py
    -> 04_generate_report_api.py
    -> Power BI source comparison
```

## Tech Stack

- Python
- Pandas
- Scikit-learn
- VADER Sentiment
- Hugging Face Transformers (DistilBERT SST-2)
- Matplotlib
- Power BI
- Prompt-authored synthetic data generation
- Optional OpenAI / Anthropic API integration for executive-summary generation

## Repository Structure

```text
ai_marketing_pipeline/
|-- data/
|   |-- raw/
|   `-- processed/
|-- scripts/
|   |-- 01_load_data.py
|   |-- 02_vader_sentiment.py
|   |-- 02_transformer_sentiment.py
|   |-- 03_accuracy_comparison.py
|   |-- 04_topic_extraction.py
|   |-- 04_generate_social_posts.py
|   |-- 04_generate_report_api.py
|   |-- 05_score_social.py
|   |-- 05_sentiment_trend.py
|   `-- 06_combine_sources.py
|-- reports/
|-- powerbi/
`-- screenshots/
```

Compatibility wrappers are also retained for the original day-by-day file references:

- `scripts/01_vader_sentiment.py`
- `scripts/03_generate_report.py`
- `scripts/05_sentiment_social.py`

## Key Outputs

- `data/processed/reviews_vader.csv`
- `data/processed/reviews_bert.csv`
- `data/processed/model_comparison.csv`
- `data/processed/negative_topics.csv`
- `data/processed/social_posts_raw.csv`
- `data/processed/social_posts_bert.csv`
- `data/processed/combined_sentiment.csv`
- `reports/sentiment_report_latest.txt`
- `reports/combined_sentiment_report_latest.txt`
- `reports/sentiment_trend.png`
- `powerbi/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.pbix`

## Final Project Results

| Area | Result |
| --- | --- |
| Raw review sample | 5,000 Amazon reviews loaded |
| Modelled review sample | 1,000 reviews scored with DistilBERT |
| Review sentiment split | 693 positive / 307 negative |
| Social extension | 500 FreshBasket UK posts generated |
| Combined dataset | 1,500 rows with `source` column |
| Average DistilBERT confidence | 0.9754 |
| Trend window | 74 months from Feb 2005 to Oct 2012 |

One important modelling note: the DistilBERT checkpoint used here is binary, so neutral-style social posts are still forced into positive or negative labels during scoring. The raw generator still targets a mixed positive, negative, and neutral post design for the Day 57 requirement.

## What To Review First

- `README.md` for the project story and architecture
- `reports/combined_sentiment_report_latest.txt` for the business-style output
- `reports/sentiment_trend.png` for the time-series visual
- `screenshots/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.png` for the Power BI dashboard
- `project_notes.md` and `RETROSPECTIVE.md` for the evaluation and reflection

## How To Run

### 1. Clone the repo and prepare the raw data

Place the Amazon review source file at `data/raw/reviews.csv`. Processed sample outputs are already included so the repo is still reviewable even if a reviewer does not rerun the transformer step locally.

### 2. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

Optional: if you want the report generator to call a hosted model for the Day 56 executive summary, export either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` before running the pipeline. Without a key, the repo falls back to a local deterministic summary so the workflow still completes end to end.

## Power BI

- Dashboard file: `powerbi/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.pbix`
- Screenshot: `screenshots/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.png`

![AI Marketing Pipeline dashboard](screenshots/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.png)

## Documentation Added For Days 58-60

- `project_notes.md` for the accuracy comparison write-up
- `presentation_notes.md` for the five-minute verbal walkthrough
- `RETROSPECTIVE.md` for the end-of-project review

## Recruiter Notes

This project is designed to show practical analytics engineering judgement rather than just model usage. The strongest examples of that are:

- choosing BERT because negative sentiment capture matters more than slightly higher overall accuracy
- restructuring the repo into a repeatable pipeline instead of leaving it as a loose set of experiments
- replacing an impractical local LLM workflow with a cleaner, lighter multi-source architecture
- packaging the work with reports, dashboard assets, and presentation notes so the output is understandable to non-technical stakeholders