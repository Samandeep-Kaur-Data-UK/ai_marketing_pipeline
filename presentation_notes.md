# Project 2: AI Marketing Pipeline - 5-Minute Verbal Walkthrough

## Opening (30 seconds)

"This project turns unstructured customer text into a marketing reporting workflow. I used 5,000 Amazon Fine Food reviews for the base dataset, scored a 1,000-review modelling sample with VADER and DistilBERT, and then added 500 simulated FreshBasket UK social posts so the final dashboard could compare sentiment across two sources."

## Part 1: The Business Problem and Data (60 seconds)

"Marketing teams cannot manually read thousands of reviews and comments every week. They need a repeatable way to measure sentiment, spot complaint themes, and understand whether a change in customer feedback is isolated or widespread. I built that workflow in Python using Amazon reviews as the main input, then extended it with a synthetic social source to make the project closer to a real cross-channel marketing pipeline."

## Part 2: The Model Comparison (90 seconds)

"I deliberately compared two sentiment approaches. VADER gave me a fast, rule-based baseline. DistilBERT gave me a contextual transformer model. When I used star ratings as a proxy for ground truth, VADER achieved 86.4% overall accuracy and DistilBERT achieved 85.0%. But the more important result was the negative class: DistilBERT reached a negative F1 score of 0.652 compared with 0.531 for VADER. For a marketing team, missing negative feedback is more costly than losing a small amount of overall accuracy, so DistilBERT became the production model for reporting."

## Part 3: The Day 56-57 Pivot (60 seconds)

"Mid-project I moved away from a heavier local model-hosting setup because it was not reliable on my hardware. The final repo is cleaner and more stable: the report generator is Claude or GPT API-ready with a local fallback, and the FreshBasket UK social dataset is produced through a Codex-assisted workflow instead of a local model server. That let me keep the multi-source analytics idea without leaving the project dependent on heavy local LLM infrastructure."

## Part 4: Reporting and Dashboard Output (60 seconds)

"The pipeline writes a dated sentiment report, extracts negative themes with TF-IDF, produces a sentiment trend chart, and prepares a Power BI dashboard. The Day 57 extension creates a combined dataset with 1,500 records and a `source` column, so review sentiment and social sentiment can be compared side by side. The Day 56 report step also appends a three-paragraph executive summary with two recommendations, using Claude or GPT when API keys are available."

## Closing (30 seconds)

"The finished repo is organised, reproducible, and portfolio-ready. It includes the cleaned scripts, processed outputs, dashboard files, walkthrough notes, and retrospective. I would position it as a practical analytics engineering project that shows model evaluation, automation, and business communication in one workflow."

## Interview Q&A Preparation

**Q1: How would you deploy this pipeline to run daily in a business?**  
"I would containerise the Python workflow, schedule it with cron, GitHub Actions, or a cloud function, and point the inputs at APIs or cloud storage rather than local CSV drops. The run would refresh processed outputs, regenerate the report, and then trigger a Power BI refresh."

**Q2: What are the limitations of BERT sentiment analysis?**  
"The main limitations are compute cost, inference time at scale, and domain fit. DistilBERT is much better than VADER on nuanced language, but it is still a general sentiment model, so I would want domain-specific validation or fine-tuning before using it for higher-stakes brand decisions."

**Q3: How would you handle 1 million reviews?**  
"I would move from one-machine CSV processing to chunked ingestion, batched inference on GPU-backed infrastructure, and storage in a database or lakehouse table. I would also split the fast baseline monitoring layer from the deeper transformer layer so reporting stays efficient."

**Q4: What would you do if sentiment suddenly dropped 20% week on week?**  
"First I would rule out a pipeline or source issue. Then I would break the drop down by source, product area, and recurring complaint themes, compare it with the previous week, and send a short incident summary to product, customer care, and marketing so the likely root cause can be addressed quickly."

## Key Numbers To Remember

- 5,000 Amazon reviews loaded for the base dataset
- 1,000 reviews scored with DistilBERT for the model comparison and reporting workflow
- 500 FreshBasket UK social posts generated for the Day 57 extension
- 1,500 combined records in the final cross-source dataset
- 86.4% VADER accuracy versus 85.0% DistilBERT accuracy
- 0.531 VADER negative F1 versus 0.652 DistilBERT negative F1
