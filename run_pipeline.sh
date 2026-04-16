#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
RUN_DATE="$(date +%F)"

if [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
  "$PYTHON_BIN" -m pip install -r requirements.txt --quiet
elif [ -x "venv/bin/python" ]; then
  PYTHON_BIN="venv/bin/python"
  "$PYTHON_BIN" -m pip install -r requirements.txt --quiet
else
  PYTHON_BIN="python3"
  "$PYTHON_BIN" -m pip install -r requirements.txt --break-system-packages --quiet
fi

echo "================================================"
echo "AI Marketing Pipeline - Starting Full Run"
echo "================================================"

echo ""
echo "Using Python interpreter: $PYTHON_BIN"
echo "Packages ready."

echo ""
echo "Step 1: Loading raw data..."
"$PYTHON_BIN" scripts/01_load_data.py
echo "Step 1 complete."

echo ""
echo "Step 2: Running VADER sentiment analysis..."
"$PYTHON_BIN" scripts/02_vader_sentiment.py
echo "Step 2 complete."

echo ""
echo "Step 3: Running BERT transformer sentiment..."
"$PYTHON_BIN" scripts/02_transformer_sentiment.py
echo "Step 3 complete."

echo ""
echo "Step 4: Comparing VADER vs BERT accuracy..."
"$PYTHON_BIN" scripts/03_accuracy_comparison.py
echo "Step 4 complete."

echo ""
echo "Step 5: Extracting negative review themes..."
"$PYTHON_BIN" scripts/04_topic_extraction.py
echo "Step 5 complete."

echo ""
echo "Step 6: Generating review sentiment report..."
"$PYTHON_BIN" scripts/04_generate_report_api.py \
  --date "$RUN_DATE" \
  --input data/processed/reviews_bert.csv \
  --title "SENTIMENT ANALYSIS REPORT"
echo "Step 6 complete."

echo ""
echo "Step 7: Generating sentiment trend chart..."
"$PYTHON_BIN" scripts/05_sentiment_trend.py
echo "Step 7 complete."

echo ""
echo "Step 8: Generating simulated social posts..."
"$PYTHON_BIN" scripts/04_generate_social_posts.py
echo "Step 8 complete."

echo ""
echo "Step 9: Running sentiment analysis on social posts..."
"$PYTHON_BIN" scripts/05_score_social.py
echo "Step 9 complete."

echo ""
echo "Step 10: Combining review and social sentiment outputs..."
"$PYTHON_BIN" scripts/06_combine_sources.py
echo "Step 10 complete."

echo ""
echo "Step 11: Generating combined sentiment report..."
"$PYTHON_BIN" scripts/04_generate_report_api.py \
  --date "$RUN_DATE" \
  --input data/processed/combined_sentiment.csv \
  --text-column review_text \
  --output "reports/combined_sentiment_report_${RUN_DATE}.txt" \
  --title "COMBINED SENTIMENT REPORT"
echo "Step 11 complete."

cp "reports/sentiment_report_${RUN_DATE}.txt" "reports/sentiment_report_latest.txt"
cp "reports/combined_sentiment_report_${RUN_DATE}.txt" "reports/combined_sentiment_report_latest.txt"

echo ""
echo "================================================"
echo "Pipeline complete. Latest reports refreshed in reports/."
echo "================================================"
