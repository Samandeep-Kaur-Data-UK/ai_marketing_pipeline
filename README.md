# AI Marketing Pipeline

**120-Day Data Analytics Journey - Project 2 (Days 46-60)**

## Project Overview
An end-to-end AI-powered pipeline that analyses thousands of customer reviews 
using sentiment analysis and automates a business-ready report.

## Business Problem
Manually reading thousands of customer reviews is not scalable. 
This pipeline automatically classifies reviews as Positive, Negative, or Neutral 
and surfaces actionable insights for marketing teams.

## Dataset
- Source: Amazon Fine Food Reviews (Kaggle)
- Size: 5,000 reviews
- Key columns: Text (review), Score (1-5 stars), Summary

## Tech Stack
- Python 3.14 / Pandas 3.0
- Sentiment Analysis: VADER / HuggingFace Transformers (DistilBERT)
- Visualisation: Power BI (DAX measures, Word Cloud visual)
- Automation: Python scripted pipeline

## Scripts
| Script | Purpose |
|---|---|
| 01_load_data.py | Load and inspect raw reviews |
| 02_vader_sentiment.py | Rule-based sentiment baseline using VADER |
| 02_transformer_sentiment.py | BERT deep learning sentiment analysis |
| 03_accuracy_comparison.py | Compare VADER vs BERT accuracy |
| 03_generate_report.py | Automated sentiment report generator |
| 04_topic_extraction.py | TF-IDF topic extraction from negative reviews |
| 05_sentiment_trend.py | Monthly positive sentiment trend chart |

## Power BI Dashboard
**File:** `powerbi/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.pbix`

**Screenshot:** `screenshots/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.png`

**Dashboard visuals:**
- 4 KPI cards: Total Reviews Analysed, Positive Sentiment Rate, Negative Sentiment Rate, Avg BERT Confidence Score
- Sentiment Distribution bar chart (positive / neutral / negative)
- Monthly Positive Sentiment Trend line chart (January to December)
- Review Keywords Word Cloud (Microsoft AppSource visual)

**DAX Measures created:**
```
Total Reviews = COUNTROWS(reviews_bert)
Positive Reviews = CALCULATE([Total Reviews], reviews_bert[bert_label] = "POSITIVE")
% Positive = DIVIDE([Positive Reviews], [Total Reviews], 0)
Negative Reviews = CALCULATE([Total Reviews], reviews_bert[bert_label] = "NEGATIVE")
% Negative = DIVIDE([Negative Reviews], [Total Reviews], 0)
Avg Confidence = AVERAGE(reviews_bert[bert_score])
ReviewDate = DATE(1970, 1, 1) + (reviews_bert[Time] / 86400)
```

---

## Key Results

### Day 46 - Setup and Data Load
| Item | Detail |
|---|---|
| Dataset | Amazon Fine Food Reviews (Kaggle) |
| Raw file | data/raw/reviews.csv |
| Total reviews loaded | 5,000 |
| Key columns | Id, ProductId, UserId, Score, Summary, Text |
| Script | 01_load_data.py |

**Finding:** Raw dataset loaded and inspected. 5,000 reviews confirmed with
star ratings (1-5) and free text fields available for sentiment analysis.
Pipeline structure established for Days 47-60.

---

### Day 47 - VADER Sentiment Baseline
| Sentiment | Count | % |
|---|---|---|
| Positive | 4,385 | 87.7% |
| Negative | 499 | 10.0% |
| Neutral | 116 | 2.3% |

**Average compound score by star rating:**
| Stars | Avg Score |
|---|---|
| 1 star | 0.042 |
| 2 stars | 0.253 |
| 3 stars | 0.440 |
| 4 stars | 0.729 |
| 5 stars | 0.794 |

**Finding:** VADER misclassifies 1 and 2 star reviews as positive/neutral.
This is the baseline limitation - improvement will be measured against this.

---

### Day 48 - BERT Transformer Sentiment
| Model | POSITIVE | NEGATIVE |
|---|---|---|
| DistilBERT | 693 | 307 |

**VADER vs BERT agreement:**
| Metric | Result |
|---|---|
| Agreement rate | 77.3% |
| Disagreement rate | 22.7% |
| Reviews processed | 1,000 |

**Finding:** 22.7% of reviews were labelled differently by BERT vs VADER.
BERT uses deep learning context; VADER uses rules. Day 49 confirms
which model is more accurate using star ratings as ground truth.

---

### Day 49 - Accuracy Comparison: VADER vs BERT
| Model | Accuracy | Positive F1 | Negative F1 |
|---|---|---|---|
| VADER | 86.4% | 0.926 | 0.531 |
| BERT | 85.0% | 0.904 | 0.652 |

**VADER - Detailed results:**
| Class | Precision | Recall | F1 |
|---|---|---|---|
| POSITIVE | 0.91 | 0.94 | 0.93 |
| NEGATIVE | 0.67 | 0.44 | 0.53 |

**BERT - Detailed results:**
| Class | Precision | Recall | F1 |
|---|---|---|---|
| POSITIVE | 0.98 | 0.84 | 0.90 |
| NEGATIVE | 0.51 | 0.90 | 0.65 |

**Finding:** VADER wins on overall accuracy (86.4% vs 85.0%) but BERT
is significantly better at catching negative reviews (F1 0.65 vs 0.53).
For a marketing team, missing negative reviews is costly - BERT is the
better production choice despite slightly lower overall accuracy.

---

### Day 50 - Topic Extraction from Negative Reviews
| Rank | Keyword | TF-IDF Score |
|---|---|---|
| 1 | br (HTML artifact) | 49.76 |
| 2 | like | 40.49 |
| 3 | chips | 37.40 |
| 4 | taste | 37.39 |
| 5 | good | 27.27 |
| 6 | product | 27.00 |
| 7 | food | 25.34 |
| 8 | bag | 22.11 |
| 9 | flavor | 20.49 |
| 10 | sugar | 16.73 |

**Finding:** Top negative themes centre around product taste, packaging
(bag/bags), and flavour disappointment. "br" is an HTML artifact from
raw review text - not a real keyword. "chips" suggests a specific product
category driving negative sentiment.

---

### Day 51 - Automated Sentiment Report (Python to Text File)

**Script:** `scripts/03_generate_report.py`
**Input:** `data/processed/reviews_bert.csv`
**Output:** `reports/sentiment_report_2026-04-10.txt`

| Metric | Result |
|---|---|
| Total Reviews Analysed | 1,000 |
| Avg BERT Confidence | 0.9754 |
| VADER/BERT Agreement | 77.3% |
| Positive Reviews | 693 (69.3%) |
| Negative Reviews | 307 (30.7%) |

**Top 5 Positive Themes:** chips, great, flavor, love, taste

**Top 5 Negative Themes:** chips, taste, food, product, flavor

**Finding:** Automation delivers a full sentiment report in one terminal command - `python scripts/03_generate_report.py`. Taste inconsistency is the core complaint driver across both positive and negative reviews.

---

### Day 52 - Sentiment Trend Analysis Over Time

**Script:** `scripts/05_sentiment_trend.py`
**Output:** `reports/sentiment_trend.png`

| Metric | Result |
|---|---|
| Date range | Feb 2005 to Oct 2012 |
| Months included | 74 |
| Average monthly BERT score | 0.975 |
| Lowest month | Nov 2006 (0.853) |
| Highest month | Jun 2007 (1.000) |

**Finding:** Sentiment confidence stays consistently high across most months,
with a clear early dip in late 2006 before stabilising near the 0.975 average.

---

### Day 53 - Power BI Sentiment Dashboard

**File:** `powerbi/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.pbix`
**Screenshot:** `screenshots/Project2_AI_Sentiment_Dashboard_BERT_Day53_v1.png`

| KPI | Result |
|---|---|
| Total Reviews Analysed | 1,000 |
| Positive Sentiment Rate | 69% |
| Negative Sentiment Rate | 31% |
| Avg BERT Confidence Score | 0.98 |

**Dashboard pages:** Single-page sentiment dashboard with 4 KPI cards,
sentiment distribution bar chart, monthly trend line chart, and word cloud.

**Finding:** 69% of Amazon Fine Food reviews carry positive sentiment with
an average BERT confidence of 0.98 - indicating the model is highly certain
in its classifications. Sentiment dips in mid-year months (August to October)
suggesting seasonal variation in customer satisfaction.

---

## Status
- [x] Day 46 - Setup and data load
- [x] Day 47 - VADER sentiment baseline
- [x] Day 48 - BERT transformer sentiment (77.3% VADER agreement)
- [x] Day 49 - Accuracy comparison (VADER 86.4% vs BERT 85.0%)
- [x] Day 50 - Topic extraction (307 negative reviews, top theme: taste/packaging)
- [x] Day 51 - Automate sentiment report (1,000 reviews, one terminal command)
- [x] Day 52 - Sentiment trend analysis (74 months, avg 0.975 BERT score)
- [x] Day 53 - Power BI dashboard (4 KPIs, bar chart, trend line, word cloud)
