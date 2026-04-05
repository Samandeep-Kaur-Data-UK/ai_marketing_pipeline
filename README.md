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