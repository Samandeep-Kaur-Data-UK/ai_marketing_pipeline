# Project 2: AI Marketing Pipeline — 5-Minute Verbal Walkthrough

## Opening (30 seconds)
"I built an end-to-end AI marketing pipeline using 568,000 Amazon Fine Food Reviews.
The goal was to automate customer sentiment analysis and generate executive-level
insight reports — the kind of workflow a marketing analytics team would run weekly
to monitor brand health."

---

## Part 1: The Data and Cleaning (60 seconds)
"I started with raw review data — over half a million rows with text, ratings,
helpfulness votes, and timestamps. I cleaned and validated the data using Python
and Pandas, removing nulls and ensuring data types were correct. The cleaned
dataset became the foundation for all downstream analysis."

---

## Part 2: Sentiment Analysis — Two Methods (90 seconds)
"I ran two sentiment models side by side:

- VADER: a rule-based model, fast and interpretable, good for short text
- DistilBERT: a transformer-based deep learning model, more accurate on
  nuanced language

I compared results from both and found that BERT caught sarcasm and complex
phrasing that VADER missed. In a commercial setting, I would use VADER for
real-time dashboards and BERT for deeper periodic analysis."

---

## Part 3: Multi-Source Pipeline (60 seconds)
"I extended the pipeline to handle two data sources — the Amazon reviews and
a simulated set of 500 social media posts. Each record was tagged with a source
column. This mirrors how a real marketing team aggregates data from multiple
channels: reviews, social, surveys. The combined dataset was then pushed into
Power BI for visual comparison by source."

---

## Part 4: Automated Report Generation (45 seconds)
"The final script auto-generates a structured sentiment report — positive,
neutral and negative breakdowns, top themes, and an AI-written executive
summary with two actionable recommendations. This report runs in one command
and outputs a dated text file. In a business context this replaces hours of
manual reporting."

---

## Closing (30 seconds)
"The full pipeline — cleaning, sentiment scoring, multi-source aggregation,
automated reporting, and Power BI dashboard — is documented on GitHub with
a README, architecture overview, requirements.txt, and screenshots. I can
walk through any part of the code in detail."

---

## Interview Q&A Preparation

**Q1: How would you deploy this pipeline to run daily in a business?**
"I would schedule the Python scripts using cron on a Linux server or Azure
Functions. The script would pull fresh review data via API each morning,
run sentiment scoring, generate the report, and email it to stakeholders
automatically. The Power BI dashboard would refresh from the updated data
source."

**Q2: What are the limitations of BERT sentiment analysis?**
"Three main ones: it is computationally expensive at scale, it requires a
GPU for fast inference on large datasets, and it was fine-tuned on general
text so domain-specific language like food industry jargon may reduce
accuracy. For production I would fine-tune on domain data."

**Q3: How would you handle 1 million reviews?**
"I would process in batches using pandas chunking with pd.read_csv chunksize
parameter, run BERT inference in batches on a GPU, and store results
incrementally to SQLite or PostgreSQL rather than holding everything in memory."

**Q4: What would you do if sentiment suddenly dropped 20% week on week?**
"First I would check for data pipeline issues — missing data or a source
change. If the data is clean I would drill into which product category or
source drove the drop, identify the specific negative themes using topic
modelling, and flag it to the marketing team with a recommended response
such as a product review or campaign adjustment."

---

## Key Numbers to Remember
- 568,000 reviews analysed
- 2 sentiment models: VADER and DistilBERT
- 2 data sources: reviews and social simulation
- 1 automated report generated per run
- Full pipeline runs in a single terminal command