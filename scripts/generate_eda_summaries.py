from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path("/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj")
OUTPUT_DIR = ROOT / "eda_outputs"

GENZ_PATH = ROOT / "genz_slang_usage_2020_2025.csv"
TWITTER_2010_PATH = ROOT / "2010_tweets_slang_analysis_ready.csv"
TWITTER_2010_TERM_TABLE_PATH = ROOT / "tweets data prep" / "2010_terms_annotation_table.csv"

VOWEL_GROUP_RE = re.compile(r"[aeiouy]+", re.IGNORECASE)
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
ACRONYM_RE = re.compile(r"^[A-Z]{2,}$")


def count_syllables(text: str) -> int:
    text = (text or "").strip().lower()
    if not text:
        return 0

    tokens = re.findall(r"[a-z]+", text)
    if not tokens:
        return 0

    total = 0
    for token in tokens:
        groups = VOWEL_GROUP_RE.findall(token)
        syllables = len(groups)
        if token.endswith("e") and not token.endswith(("le", "ye")) and syllables > 1:
            syllables -= 1
        total += max(1, syllables)
    return total


def is_acronym(text: str) -> bool:
    value = (text or "").strip()
    if not value:
        return False
    return bool(ACRONYM_RE.fullmatch(value))


def bucket_syllables(value: int) -> str:
    if value <= 1:
        return "1"
    if value == 2:
        return "2"
    return "3+"


def add_term_features(df: pd.DataFrame, term_col: str) -> pd.DataFrame:
    enriched = df.copy()
    enriched["normalized_term"] = enriched[term_col].astype(str).str.strip().str.lower()
    enriched["char_count"] = enriched[term_col].astype(str).str.len()
    enriched["token_count"] = enriched[term_col].astype(str).apply(lambda value: len(TOKEN_RE.findall(value)))
    enriched["syllable_count"] = enriched[term_col].astype(str).apply(count_syllables)
    enriched["syllable_bucket"] = enriched["syllable_count"].apply(bucket_syllables)
    enriched["is_acronym"] = enriched[term_col].astype(str).apply(is_acronym)
    enriched["is_multiword"] = enriched["token_count"] > 1
    return enriched


def write_csv(df: pd.DataFrame, filename: str) -> None:
    target = OUTPUT_DIR / filename
    df.to_csv(target, index=False)
    print(f"Wrote {len(df):>6} rows to {target}")


def summarize_group_counts(
    df: pd.DataFrame,
    group_cols: list[str],
    term_col: str,
    value_name: str = "posts",
) -> pd.DataFrame:
    summary = (
        df.groupby(group_cols, dropna=False)
        .agg(
            **{
                value_name: (term_col, "size"),
                "unique_terms": (term_col, "nunique"),
            }
        )
        .reset_index()
        .sort_values(value_name, ascending=False)
    )
    return summary


def build_genz_outputs() -> pd.DataFrame:
    genz = pd.read_csv(GENZ_PATH, parse_dates=["timestamp"])
    genz = add_term_features(genz, "slang_term")
    genz["year"] = genz["timestamp"].dt.year
    genz["month"] = genz["timestamp"].dt.to_period("M").astype(str)

    write_csv(
        summarize_group_counts(genz, ["year", "origin_platform"], "slang_term"),
        "genz_year_origin_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(genz, ["year", "usage_platform"], "slang_term"),
        "genz_year_usage_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(genz, ["region", "origin_platform"], "slang_term"),
        "genz_region_origin_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(genz, ["user_age_group", "origin_platform"], "slang_term"),
        "genz_age_origin_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(genz, ["term_category", "origin_platform"], "slang_term"),
        "genz_category_origin_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(genz, ["term_category", "usage_platform"], "slang_term"),
        "genz_category_usage_platform_summary.csv",
    )

    syllable_year = (
        genz.groupby(["year", "syllable_bucket"], dropna=False)
        .agg(
            posts=("record_id", "count"),
            unique_terms=("normalized_term", "nunique"),
            avg_syllables=("syllable_count", "mean"),
            avg_chars=("char_count", "mean"),
        )
        .reset_index()
        .sort_values(["year", "syllable_bucket"])
    )
    write_csv(syllable_year, "genz_syllable_by_year_summary.csv")

    syllable_region = (
        genz.groupby(["region", "syllable_bucket"], dropna=False)
        .agg(posts=("record_id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("posts", ascending=False)
    )
    write_csv(syllable_region, "genz_syllable_by_region_summary.csv")

    syllable_age = (
        genz.groupby(["user_age_group", "syllable_bucket"], dropna=False)
        .agg(posts=("record_id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("posts", ascending=False)
    )
    write_csv(syllable_age, "genz_syllable_by_age_summary.csv")

    syllable_category = (
        genz.groupby(["term_category", "syllable_bucket"], dropna=False)
        .agg(posts=("record_id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("posts", ascending=False)
    )
    write_csv(syllable_category, "genz_syllable_by_category_summary.csv")

    efficiency_year = (
        genz.groupby("year", dropna=False)
        .agg(
            posts=("record_id", "count"),
            unique_terms=("normalized_term", "nunique"),
            avg_syllables=("syllable_count", "mean"),
            median_syllables=("syllable_count", "median"),
            avg_chars=("char_count", "mean"),
            acronym_share=("is_acronym", "mean"),
            multiword_share=("is_multiword", "mean"),
            avg_sentiment_score=("sentiment_score", "mean"),
            avg_days_since_emergence=("days_since_emergence", "mean"),
        )
        .reset_index()
    )
    write_csv(efficiency_year, "genz_efficiency_by_year_summary.csv")

    lifecycle = (
        genz.groupby(["slang_term", "lifecycle_phase"], dropna=False)
        .agg(
            posts=("record_id", "count"),
            avg_virality_score=("virality_score", "mean"),
            avg_sentiment_score=("sentiment_score", "mean"),
            avg_days_since_emergence=("days_since_emergence", "mean"),
        )
        .reset_index()
        .sort_values(["slang_term", "posts"], ascending=[True, False])
    )
    write_csv(lifecycle, "genz_lifecycle_term_summary.csv")

    trajectory = (
        genz.groupby(["month", "slang_term"], dropna=False)
        .agg(
            posts=("record_id", "count"),
            avg_sentiment_score=("sentiment_score", "mean"),
            avg_virality_score=("virality_score", "mean"),
        )
        .reset_index()
        .sort_values(["slang_term", "month"])
    )
    write_csv(trajectory, "genz_term_monthly_trajectory.csv")

    sentiment_platform = (
        genz.groupby(["origin_platform", "sentiment"], dropna=False)
        .agg(posts=("record_id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("posts", ascending=False)
    )
    write_csv(sentiment_platform, "genz_sentiment_by_origin_platform.csv")

    sentiment_category = (
        genz.groupby(["term_category", "sentiment"], dropna=False)
        .agg(
            posts=("record_id", "count"),
            unique_terms=("normalized_term", "nunique"),
            avg_sentiment_score=("sentiment_score", "mean"),
        )
        .reset_index()
        .sort_values("posts", ascending=False)
    )
    write_csv(sentiment_category, "genz_sentiment_by_category.csv")

    return genz


def build_2010_outputs() -> pd.DataFrame:
    twitter_2010 = pd.read_csv(TWITTER_2010_PATH, parse_dates=["date"])
    term_table = pd.read_csv(TWITTER_2010_TERM_TABLE_PATH)

    twitter_2010 = add_term_features(twitter_2010, "word")
    twitter_2010["year"] = twitter_2010["date"].dt.year
    twitter_2010["month"] = twitter_2010["date"].dt.to_period("M").astype(str)

    twitter_2010 = twitter_2010.merge(
        term_table[["word", "origin_platform", "origin_platform_confidence", "tweet_count"]],
        on="word",
        how="left",
    )

    write_csv(
        summarize_group_counts(twitter_2010, ["origin_platform"], "word", value_name="tweets"),
        "twitter2010_origin_platform_summary.csv",
    )
    write_csv(
        summarize_group_counts(twitter_2010, ["term_category"], "word", value_name="tweets"),
        "twitter2010_category_summary.csv",
    )
    write_csv(
        summarize_group_counts(twitter_2010, ["usage_context"], "word", value_name="tweets"),
        "twitter2010_usage_context_summary.csv",
    )

    platform_category = (
        twitter_2010.groupby(["origin_platform", "term_category"], dropna=False)
        .agg(tweets=("id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("tweets", ascending=False)
    )
    write_csv(platform_category, "twitter2010_origin_platform_by_category.csv")

    acronym = (
        twitter_2010.groupby("is_acronym", dropna=False)
        .agg(tweets=("id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
    )
    write_csv(acronym, "twitter2010_acronym_summary.csv")

    syllables = (
        twitter_2010.groupby(["term_category", "syllable_bucket"], dropna=False)
        .agg(tweets=("id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
        .sort_values("tweets", ascending=False)
    )
    write_csv(syllables, "twitter2010_syllable_by_category_summary.csv")

    timeline = (
        twitter_2010.groupby(["month", "word"], dropna=False)
        .agg(tweets=("id", "count"), ironic_share=("is_ironic", "mean"))
        .reset_index()
        .sort_values(["word", "month"])
    )
    write_csv(timeline, "twitter2010_term_monthly_trajectory.csv")

    efficiency = (
        twitter_2010.groupby("month", dropna=False)
        .agg(
            tweets=("id", "count"),
            unique_terms=("normalized_term", "nunique"),
            avg_syllables=("syllable_count", "mean"),
            median_syllables=("syllable_count", "median"),
            avg_chars=("char_count", "mean"),
            acronym_share=("is_acronym", "mean"),
            ironic_share=("is_ironic", "mean"),
        )
        .reset_index()
    )
    write_csv(efficiency, "twitter2010_efficiency_by_month_summary.csv")

    return twitter_2010


def build_cross_dataset_outputs(genz: pd.DataFrame, twitter_2010: pd.DataFrame) -> None:
    genz_categories = (
        genz.groupby("term_category", dropna=False)
        .agg(records=("record_id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
    )
    genz_categories["dataset"] = "genz_2020_2025"

    twitter_categories = (
        twitter_2010.groupby("term_category", dropna=False)
        .agg(records=("id", "count"), unique_terms=("normalized_term", "nunique"))
        .reset_index()
    )
    twitter_categories["dataset"] = "twitter_2010"

    category_compare = pd.concat([genz_categories, twitter_categories], ignore_index=True)
    write_csv(category_compare, "cross_dataset_category_comparison.csv")

    acronym_compare = pd.DataFrame(
        [
            {
                "dataset": "genz_2020_2025",
                "records": len(genz),
                "unique_terms": genz["normalized_term"].nunique(),
                "record_level_acronym_share": genz["is_acronym"].mean(),
                "term_level_acronym_share": genz.drop_duplicates("normalized_term")["is_acronym"].mean(),
            },
            {
                "dataset": "twitter_2010",
                "records": len(twitter_2010),
                "unique_terms": twitter_2010["normalized_term"].nunique(),
                "record_level_acronym_share": twitter_2010["is_acronym"].mean(),
                "term_level_acronym_share": twitter_2010.drop_duplicates("normalized_term")["is_acronym"].mean(),
            },
        ]
    )
    write_csv(acronym_compare, "cross_dataset_acronym_comparison.csv")

    syllable_compare = pd.DataFrame(
        [
            {
                "dataset": "genz_2020_2025",
                "records": len(genz),
                "unique_terms": genz["normalized_term"].nunique(),
                "avg_syllables_record_level": genz["syllable_count"].mean(),
                "avg_syllables_term_level": genz.drop_duplicates("normalized_term")["syllable_count"].mean(),
            },
            {
                "dataset": "twitter_2010",
                "records": len(twitter_2010),
                "unique_terms": twitter_2010["normalized_term"].nunique(),
                "avg_syllables_record_level": twitter_2010["syllable_count"].mean(),
                "avg_syllables_term_level": twitter_2010.drop_duplicates("normalized_term")["syllable_count"].mean(),
            },
        ]
    )
    write_csv(syllable_compare, "cross_dataset_syllable_comparison.csv")

    overlap = sorted(set(genz["normalized_term"]) & set(twitter_2010["normalized_term"]))
    overlap_df = pd.DataFrame({"normalized_term_overlap": overlap})
    write_csv(overlap_df, "cross_dataset_exact_term_overlap.csv")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    genz = build_genz_outputs()
    twitter_2010 = build_2010_outputs()
    build_cross_dataset_outputs(genz, twitter_2010)

    print("\nEDA summary export complete.")


if __name__ == "__main__":
    main()
