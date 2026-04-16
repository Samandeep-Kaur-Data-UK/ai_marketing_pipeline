from pathlib import Path
import runpy


# Tracker compatibility wrapper:
# Day 47 refers to scripts/01_vader_sentiment.py, while the repo kept the
# original implementation in 02_vader_sentiment.py after adding 01_load_data.py.
runpy.run_path(Path(__file__).with_name("02_vader_sentiment.py"), run_name="__main__")
