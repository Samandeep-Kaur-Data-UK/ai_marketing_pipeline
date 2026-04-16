from pathlib import Path
import runpy


# Tracker compatibility wrapper:
# Day 57 refers to scripts/05_sentiment_social.py. The portfolio-facing repo
# uses 05_score_social.py as the primary script name.
runpy.run_path(Path(__file__).with_name("05_score_social.py"), run_name="__main__")
