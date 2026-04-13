import requests
import pandas as pd
from datetime import datetime

prompt = """Write 500 social media posts about a UK online shop. 
One post per line. No headings, no categories, no numbering, no intro text.
Just 500 posts. Start with post 1 immediately."""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 8000}
    }
)

raw = response.json()["response"].strip()

# Filter out junk lines
junk_keywords = ["here are", "positive", "negative", "neutral", "posts:", "category", "---"]

posts = [
    line.strip() for line in raw.split("\n")
    if line.strip()
    and not any(kw in line.lower() for kw in junk_keywords)
    and len(line.strip()) > 15
]

print(f"Generated {len(posts)} posts.")

df_social = pd.DataFrame({
    "review_text": posts,
    "source": "social",
    "date": pd.Timestamp(datetime.today().date())
})

df_social.to_csv("data/processed/social_posts_raw.csv", index=False)
print(df_social.head(3))