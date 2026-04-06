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
- Sentiment Analysis: VADER / HuggingFace Transformers
- Visualisation: Power BI
- Automation: Python scripted pipeline

## Project Structure


## Scripts
| Script | Purpose |
|---|---|
| 01_load_data.py | Load and inspect raw reviews |
| 02_clean.py | Clean and prepare data (Day 47) |
| 03_sentiment.py | Run AI sentiment analysis (Day 48) |
| 04_report.py | Automate report generation (Day 49+) |

## Key Outputs
- Sentiment-labelled dataset (positive/negative/neutral)
- Automated summary report
- Power BI dashboard

## Status
- [x] Day 46 - Setup and data load
- [ ] Day 47 - Data cleaning
- [ ] Day 48 - Sentiment analysis
- [ ] Day 49 - Report automation

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
- Sentiment Analysis: VADER / HuggingFace Transformers
- Visualisation: Power BI
- Automation: Python scripted pipeline

## Project Structure

## Scripts
| Script | Purpose |
|---|---|
| 01_load_data.py | Load and inspect raw reviews |
| 02_vader_sentiment.py | Rule-based sentiment baseline using VADER |
| 03_clean.py | Clean and prepare data (coming Day 48+) |
| 04_report.py | Automate report generation (coming Day 49+) |

## Key Results So Far

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

## Status
- [x] Day 46 - Setup and data load
- [x] Day 47 - VADER sentiment baseline
- [ ] Day 48 - Sentiment analysis improvement
- [ ] Day 49 - Report automation

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
BERT uses deep learning context; VADER uses rules. Day 49 will confirm
which model is more accurate using star ratings as ground truth.

## Status
- [x] Day 46 - Setup and data load
- [x] Day 47 - VADER sentiment baseline
- [x] Day 48 - BERT transformer sentiment (77.3% VADER agreement)
- [ ] Day 49 - Accuracy comparison vs star ratings
- [ ] Day 50 - Report automation


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

## Status
- [x] Day 46 - Setup and data load
- [x] Day 47 - VADER sentiment baseline
- [x] Day 48 - BERT transformer sentiment (77.3% VADER agreement)
- [x] Day 49 - Accuracy comparison (VADER 86.4% vs BERT 85.0%)
- [ ] Day 50 - Topic extraction from negative reviews

### Day 50 - Topic Extraction from Negative Reviews
| Rank | Keyword | TF-IDF Score |
|---|---|---|
| 1 | br (line break artifact) | 49.76 |
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
raw review text - not a real keyword. "kettle" and "chips" suggest a
specific product category driving negative sentiment. "amazon" appearing
suggests complaints about delivery/seller, not just the product itself.

## Status
- [x] Day 46 - Setup and data load
- [x] Day 47 - VADER sentiment baseline
- [x] Day 48 - BERT transformer sentiment (77.3% VADER agreement)
- [x] Day 49 - Accuracy comparison (VADER 86.4% vs BERT 85.0%)
- [x] Day 50 - Topic extraction (307 negative reviews, top theme: taste/packaging)
- [ ] Day 51 - Automate sentiment report (Python to text file)