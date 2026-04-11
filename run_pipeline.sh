#!/bin/bash

echo "================================================"
echo "AI Marketing Pipeline - Starting Full Run"
echo "================================================"

echo ""
echo "Installing required packages..."
pip install vaderSentiment transformers torch --break-system-packages --quiet
echo "Packages ready."

echo ""
echo "Step 1: Loading raw data..."
python scripts/01_load_data.py
echo "Step 1 complete."

echo ""
echo "Step 2: Running VADER sentiment analysis..."
python scripts/02_vader_sentiment.py
echo "Step 2 complete."

echo ""
echo "Step 3: Running BERT transformer sentiment..."
python scripts/02_transformer_sentiment.py
echo "Step 3 complete."

echo ""
echo "Step 4: Generating sentiment report..."
python scripts/03_generate_report.py
echo "Step 4 complete."

echo ""
echo "Step 5: Generating sentiment trend chart..."
python scripts/05_sentiment_trend.py
echo "Step 5 complete."

echo ""
echo "================================================"
echo "Pipeline complete. Check reports/ for outputs."
echo "================================================"