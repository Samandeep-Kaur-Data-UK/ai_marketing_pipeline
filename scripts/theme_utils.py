from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS


CUSTOM_THEME_STOP_WORDS = {
    "amazon",
    "bit",
    "bought",
    "br",
    "buy",
    "did",
    "does",
    "dog",
    "don",
    "even",
    "food",
    "freshbasket",
    "getting",
    "got",
    "good",
    "great",
    "item",
    "items",
    "just",
    "know",
    "like",
    "ll",
    "lot",
    "make",
    "one",
    "order",
    "ordered",
    "ordering",
    "product",
    "products",
    "really",
    "review",
    "reviews",
    "shopping",
    "store",
    "best",
    "better",
    "thing",
    "things",
    "time",
    "today",
    "tried",
    "trying",
    "try",
    "uk",
    "use",
    "used",
    "using",
    "ve",
    "way",
    "week",
    "weeks",
    "love",
    "work",
    "would",
}

STOP_WORDS = sorted(set(ENGLISH_STOP_WORDS).union(CUSTOM_THEME_STOP_WORDS))


def clean_text_series(series: pd.Series) -> pd.Series:
    return (
        series.dropna()
        .astype(str)
        .str.replace(r"<br\s*/?>", " ", regex=True)
        .str.replace(r"[^A-Za-z\s]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def _canonical_tokens(term: str) -> frozenset[str]:
    tokens = []
    for token in term.split():
        if len(token) > 3 and token.endswith("s"):
            tokens.append(token[:-1])
        else:
            tokens.append(token)
    return frozenset(tokens)


def _select_distinct_terms(scored_terms: Iterable[tuple[str, float]], n: int) -> list[str]:
    selected_terms: list[str] = []
    selected_token_sets: list[frozenset[str]] = []

    for term, _ in scored_terms:
        token_set = _canonical_tokens(term)
        if not token_set:
            continue
        if any(token_set <= existing or existing <= token_set for existing in selected_token_sets):
            continue

        selected_terms.append(term)
        selected_token_sets.append(token_set)
        if len(selected_terms) == n:
            break

    return selected_terms


def build_theme_frame(
    df: pd.DataFrame,
    *,
    label_col: str,
    label_value: str,
    text_col: str,
    min_df: int = 3,
) -> pd.DataFrame:
    subset = clean_text_series(df.loc[df[label_col] == label_value, text_col])
    if subset.empty:
        return pd.DataFrame(columns=["keyword", "score"])

    vectorizer = CountVectorizer(
        stop_words=STOP_WORDS,
        ngram_range=(1, 2),
        min_df=min_df,
        max_features=300,
    )

    try:
        matrix = vectorizer.fit_transform(subset)
    except ValueError:
        return pd.DataFrame(columns=["keyword", "score"])

    theme_frame = pd.DataFrame(
        {
            "keyword": vectorizer.get_feature_names_out(),
            "score": matrix.sum(axis=0).A1,
        }
    )
    theme_frame["adjusted_score"] = theme_frame["score"] * theme_frame["keyword"].str.contains(" ").map(
        lambda is_bigram: 1.15 if is_bigram else 1.0
    )
    return theme_frame.sort_values(
        by=["adjusted_score", "score", "keyword"],
        ascending=[False, False, True],
    ).reset_index(drop=True)


def extract_top_themes(
    df: pd.DataFrame,
    *,
    label_col: str,
    label_value: str,
    text_col: str,
    n: int = 5,
    min_df: int = 3,
) -> list[str]:
    theme_frame = build_theme_frame(
        df,
        label_col=label_col,
        label_value=label_value,
        text_col=text_col,
        min_df=min_df,
    )
    if theme_frame.empty:
        return []

    scored_terms = list(zip(theme_frame["keyword"], theme_frame["adjusted_score"]))
    return _select_distinct_terms(scored_terms, n=n)
