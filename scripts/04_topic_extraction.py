from pathlib import Path

import pandas as pd

from theme_utils import build_theme_frame


INPUT_PATH = Path("data/processed/reviews_bert.csv")
OUTPUT_PATH = Path("data/processed/negative_topics.csv")


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    df["bert_label_norm"] = df["bert_label"].astype(str).str.upper()
    negative_count = int((df["bert_label_norm"] == "NEGATIVE").sum())
    print(f"Total negative reviews: {negative_count}")

    themes = build_theme_frame(
        df,
        label_col="bert_label_norm",
        label_value="NEGATIVE",
        text_col="Text",
        min_df=3,
    ).rename(columns={"score": "term_frequency"})

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    themes.to_csv(OUTPUT_PATH, index=False)

    if themes.empty:
        print("No negative themes were extracted from the current dataset.")
    else:
        print(themes.head(15).to_string(index=False))

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
