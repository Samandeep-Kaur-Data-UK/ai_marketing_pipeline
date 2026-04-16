from pathlib import Path
import runpy


# Tracker compatibility wrapper:
# Day 51 and Day 56 refer to scripts/03_generate_report.py. The main
# implementation now lives in 04_generate_report_api.py so the repo keeps a
# clearer separation between reporting and the earlier modelling steps.
runpy.run_path(Path(__file__).with_name("04_generate_report_api.py"), run_name="__main__")
