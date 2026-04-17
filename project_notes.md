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


## Project 2 Retrospective

### What went well
- Full pipeline from raw CSV to AI narrative runs in a single bash command
- BERT negative recall at 0.897 is the standout commercial finding - complaints are caught reliably
- Multi-source architecture (reviews + simulated social) demonstrates production thinking
- All scripts committed with descriptive day-by-day commit history

### What was hard
- Anthropic and Azure Foundry API access failed - pivoted to local Ollama/llama3.2
- Column name mismatches between scripts caused silent failures early on
- VS Code file save issue on one script - resolved via terminal Python one-liner

### What I would do differently
- Create a config.py on Day 1 with all file paths centralised
- Use Python logging module instead of print statements throughout
- Fine-tune DistilBERT on food/FMCG domain reviews for higher negative precision
- Set up proper unit tests so pipeline errors surface immediately