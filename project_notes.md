# Project 2 Notes

## Day 49 - Accuracy Comparison: VADER vs BERT

Ground truth mapping:
- 1-2 stars = NEGATIVE
- 3 stars = excluded as ambiguous
- 4-5 stars = POSITIVE

### Headline Results

| Model | Accuracy | Positive F1 | Negative F1 |
| --- | ---: | ---: | ---: |
| VADER | 0.864 | 0.926 | 0.531 |
| BERT | 0.850 | 0.904 | 0.652 |

### Precision and Recall by Class

#### VADER
- POSITIVE precision: 0.911
- POSITIVE recall: 0.942
- NEGATIVE precision: 0.667
- NEGATIVE recall: 0.441

#### BERT
- POSITIVE precision: 0.978
- POSITIVE recall: 0.841
- NEGATIVE precision: 0.512
- NEGATIVE recall: 0.897

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
