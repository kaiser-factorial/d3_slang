# Slang InfoViz Final Project

Observable notebook: [Slang visualization prototype](https://observablehq.com/d/5891d4faf3493260)

This project is ongoing, and both the analysis pipeline and visualization work are still being refined.

This project compares slang usage across two datasets:

- a 2020-2025 Gen Z slang dataset
- a 2010 Twitter slang dataset

The repository combines data cleaning, annotation, filtering, sentiment analysis, and exploratory summary generation for an information visualization project.

## Repository Layout

- [`scripts`](scripts): Python pipeline scripts for cleaning, annotation, filtering, export, sentiment, and EDA summary generation
- [`original`](original): raw source data snapshots
- [`tweets data prep`](tweets%20data%20prep): working files and process notes for the 2010 Twitter pipeline
- [`usage_context_batches_by_term_category`](usage_context_batches_by_term_category): category-specific usage-context annotation batches
- [`eda_outputs`](eda_outputs): derived summary tables used for exploration and visualization
- [`md_rtf`](md_rtf): project writeups, notes, and exportable presentation text
- [`slang_eda_exploration.ipynb`](slang_eda_exploration.ipynb): notebook for EDA and comparison work

## Key Data Files

- [`genz_slang_usage_2020_2025.csv`](genz_slang_usage_2020_2025.csv): main Gen Z dataset
- [`original/2010_tweets_slang.csv`](original/2010_tweets_slang.csv): raw 2010 Twitter source file
- [`2010_tweets_slang_analysis_ready.csv`](2010_tweets_slang_analysis_ready.csv): final 2010 analysis-ready dataset
- [`2010_tweets_slang_with_sentiment.csv`](2010_tweets_slang_with_sentiment.csv): analysis-ready 2010 dataset with sentiment columns added
- [`tweets data prep/2010_terms_annotation_table.csv`](tweets%20data%20prep/2010_terms_annotation_table.csv): term-level annotation table for 2010 slang

## 2010 Twitter Workflow

The 2010 Twitter dataset was built in stages:

1. clean the raw source rows
2. create a term-level annotation table
3. merge term annotations back onto tweet rows
4. annotate tweet-level usage context and irony
5. filter out rows where the word is not actually being used as slang
6. export an analysis-ready dataset
7. optionally add sentiment scores

Important note: several intermediate CSVs are still present because the scripts expect those filenames and use them as pipeline checkpoints. Some of them are logically redundant with later outputs, but they are useful if you want to rerun only one section of the workflow instead of rebuilding everything from scratch.

## Most Important Scripts

- [`scripts/clean_2010_tweets.py`](scripts/clean_2010_tweets.py)
- [`scripts/create_2010_term_table.py`](scripts/create_2010_term_table.py)
- [`scripts/annotate_2010_tweets_with_terms.py`](scripts/annotate_2010_tweets_with_terms.py)
- [`scripts/create_2010_usage_context_working_file.py`](scripts/create_2010_usage_context_working_file.py)
- [`scripts/create_2010_filtering_working_file.py`](scripts/create_2010_filtering_working_file.py)
- [`scripts/export_filtered_2010_analysis_dataset.py`](scripts/export_filtered_2010_analysis_dataset.py)
- [`scripts/export_filtered_2010_analysis_ready_dataset.py`](scripts/export_filtered_2010_analysis_ready_dataset.py)
- [`scripts/add_2010_tweet_sentiment.py`](scripts/add_2010_tweet_sentiment.py)
- [`scripts/generate_eda_summaries.py`](scripts/generate_eda_summaries.py)
