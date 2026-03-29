from __future__ import annotations

from pathlib import Path

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer


ROOT = Path("/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj")
SOURCE = ROOT / "2010_tweets_slang_analysis_ready.csv"
OUTPUT = ROOT / "2010_tweets_slang_with_sentiment.csv"
OUTPUT_SUMMARY_DIR = ROOT / "eda_outputs"


def ensure_vader() -> None:
    try:
        SentimentIntensityAnalyzer()
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


def label_from_compound(score: float) -> str:
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def main() -> None:
    ensure_vader()
    sia = SentimentIntensityAnalyzer()

    df = pd.read_csv(SOURCE)
    text = df["text"].fillna("").astype(str)
    scores = text.apply(sia.polarity_scores).apply(pd.Series)

    df["sentiment_neg"] = scores["neg"]
    df["sentiment_neu"] = scores["neu"]
    df["sentiment_pos"] = scores["pos"]
    df["sentiment_score"] = scores["compound"]
    df["sentiment_label"] = df["sentiment_score"].apply(label_from_compound)

    df.to_csv(OUTPUT, index=False)

    OUTPUT_SUMMARY_DIR.mkdir(exist_ok=True)

    by_label = (
        df.groupby("sentiment_label", dropna=False)
        .agg(tweets=("id", "count"))
        .reset_index()
        .sort_values("tweets", ascending=False)
    )
    by_label.to_csv(OUTPUT_SUMMARY_DIR / "twitter2010_sentiment_overall.csv", index=False)

    by_category = (
        df.groupby(["term_category", "sentiment_label"], dropna=False)
        .agg(
            tweets=("id", "count"),
            avg_sentiment_score=("sentiment_score", "mean"),
        )
        .reset_index()
        .sort_values("tweets", ascending=False)
    )
    by_category.to_csv(OUTPUT_SUMMARY_DIR / "twitter2010_sentiment_by_category.csv", index=False)

    by_word = (
        df.groupby("word", dropna=False)
        .agg(
            tweets=("id", "count"),
            avg_sentiment_score=("sentiment_score", "mean"),
            positive_share=("sentiment_label", lambda s: (s == "positive").mean()),
            neutral_share=("sentiment_label", lambda s: (s == "neutral").mean()),
            negative_share=("sentiment_label", lambda s: (s == "negative").mean()),
        )
        .reset_index()
        .sort_values(["tweets", "avg_sentiment_score"], ascending=[False, False])
    )
    by_word.to_csv(OUTPUT_SUMMARY_DIR / "twitter2010_sentiment_by_word.csv", index=False)

    ironic_compare = (
        df.groupby("is_ironic", dropna=False)
        .agg(
            tweets=("id", "count"),
            avg_sentiment_score=("sentiment_score", "mean"),
            positive_share=("sentiment_label", lambda s: (s == "positive").mean()),
            neutral_share=("sentiment_label", lambda s: (s == "neutral").mean()),
            negative_share=("sentiment_label", lambda s: (s == "negative").mean()),
        )
        .reset_index()
    )
    ironic_compare.to_csv(OUTPUT_SUMMARY_DIR / "twitter2010_sentiment_by_irony.csv", index=False)

    print(f"Wrote {len(df)} rows to {OUTPUT}")
    print(f"Wrote summary file: {OUTPUT_SUMMARY_DIR / 'twitter2010_sentiment_overall.csv'}")
    print(f"Wrote summary file: {OUTPUT_SUMMARY_DIR / 'twitter2010_sentiment_by_category.csv'}")
    print(f"Wrote summary file: {OUTPUT_SUMMARY_DIR / 'twitter2010_sentiment_by_word.csv'}")
    print(f"Wrote summary file: {OUTPUT_SUMMARY_DIR / 'twitter2010_sentiment_by_irony.csv'}")


if __name__ == "__main__":
    main()
