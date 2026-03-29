# Slang InfoViz Final Project

This project compares slang usage across two datasets:

- a 2020-2025 Gen Z slang dataset
- a 2010 Twitter slang dataset

The repository combines data cleaning, annotation, filtering, sentiment analysis, and exploratory summary generation for an information visualization project.

## Repository Layout

- [`scripts`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts): Python pipeline scripts for cleaning, annotation, filtering, export, sentiment, and EDA summary generation
- [`original`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/original): raw source data snapshots
- [`tweets data prep`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/tweets%20data%20prep): working files and process notes for the 2010 Twitter pipeline
- [`usage_context_batches_by_term_category`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/usage_context_batches_by_term_category): category-specific usage-context annotation batches
- [`eda_outputs`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/eda_outputs): derived summary tables used for exploration and visualization
- [`md_rtf`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/md_rtf): project writeups, notes, and exportable presentation text
- [`slang_eda_exploration.ipynb`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/slang_eda_exploration.ipynb): notebook for EDA and comparison work

## Key Data Files

- [`genz_slang_usage_2020_2025.csv`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_slang_usage_2020_2025.csv): main Gen Z dataset
- [`original/2010_tweets_slang.csv`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/original/2010_tweets_slang.csv): raw 2010 Twitter source file
- [`2010_tweets_slang_analysis_ready.csv`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_ready.csv): final 2010 analysis-ready dataset
- [`2010_tweets_slang_with_sentiment.csv`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_with_sentiment.csv): analysis-ready 2010 dataset with sentiment columns added
- [`tweets data prep/2010_terms_annotation_table.csv`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/tweets%20data%20prep/2010_terms_annotation_table.csv): term-level annotation table for 2010 slang

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

- [`scripts/clean_2010_tweets.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/clean_2010_tweets.py)
- [`scripts/create_2010_term_table.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/create_2010_term_table.py)
- [`scripts/annotate_2010_tweets_with_terms.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/annotate_2010_tweets_with_terms.py)
- [`scripts/create_2010_usage_context_working_file.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/create_2010_usage_context_working_file.py)
- [`scripts/create_2010_filtering_working_file.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/create_2010_filtering_working_file.py)
- [`scripts/export_filtered_2010_analysis_dataset.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/export_filtered_2010_analysis_dataset.py)
- [`scripts/export_filtered_2010_analysis_ready_dataset.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/export_filtered_2010_analysis_ready_dataset.py)
- [`scripts/add_2010_tweet_sentiment.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/add_2010_tweet_sentiment.py)
- [`scripts/generate_eda_summaries.py`](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/generate_eda_summaries.py)

## Suggested GitHub Scope

Good candidates to keep in the repo:

- scripts and notebook
- raw source data if you want full reproducibility
- final analysis datasets
- annotation tables and EDA outputs
- process notes and writeups

Good candidates to keep local-only:

- OS-generated files
- Python cache folders
- temporary notebook checkpoints
- any ad hoc backup or duplicate CSV exports

An ignored local archive folder is included for any redundant working exports you want to keep on your machine without pushing to GitHub.
