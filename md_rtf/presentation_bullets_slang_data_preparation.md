# Presentation-Friendly Summary

## Cleaning

- Started with a noisy 2010 Twitter slang CSV and a richer 2020-2025 Gen-Z slang CSV.
- Cleaned the 2010 dataset by fixing malformed columns, removing junk rows, and standardizing the schema.
- Combined separate `year`, `month`, and `day` fields into a single `date` field.
- Preserved 57,345 usable 2010 tweet rows after cleaning.

## Gen-Z Reference Extraction

- Extracted a Gen-Z lookup table of `(slang_term, term_category, term_meaning)`.
- Extracted the full set of Gen-Z `term_category` values.
- Extracted the full set of Gen-Z `usage_context` values.
- Used these as reference taxonomies rather than direct lookup matches.

## Term Annotation

- Built a 2010 term table with one row per unique slang term.
- Annotated all 152 terms with `term_meaning` and fixed `term_category`.
- Reused Gen-Z categories when they fit well.
- Added new category values when forcing a match would weaken the analysis.
- Standardized acronym meanings using quoted full expansions.

## Review Workflow

- Researched candidate term meanings and categories first.
- Used tweet evidence only when needed to disambiguate meaning.
- Delegated difficult cases to subagents for independent review.
- Reviewed proposed term batches manually before finalizing them.
- Revised ambiguous cases collaboratively, including terms like `gnarly`, `badass`, `twit`, and `thirsty`.

## Tweet-Level Annotation

- Added `term_meaning` and `term_category` back onto every 2010 tweet row.
- Created a tweet-level annotation workflow for `usage_context` and `is_ironic`.
- Treated `usage_context` as broader tweet/post context rather than narrow word-sense context.
- Added extra context values where the Gen-Z set was not sufficient, such as `article_sharing`, `technology_discussion`, and `sexual_context`.

## Origin Research

- Added `origin_platform` and `origin_platform_confidence` to all 152 terms.
- Researched origins using sources like Merriam-Webster, Wiktionary, Dictionary.com, Green’s Dictionary of Slang, and Know Your Meme.
- Recorded provenance in a separate research table with source links and notes.

## Row Filtering

- Built a filtering workflow to remove rows where the token appeared but was not really being used as slang.
- Used `usage_context` as a triage tool, not as an automatic drop rule.
- Kept real slang use, informal jargon, and metalinguistic slang discussion when analytically relevant.
- Dropped title shells, product references, media metadata, file-format references, and literal non-slang collisions.
- Reviewed filtering in context-by-context passes with delegated review and trailing audits.

## Final Output

- Produced a filtered 2010 dataset with 36,005 rows.
- Final analysis-ready columns:
- `word`
- `id`
- `date`
- `text`
- `author_id`
- `term_meaning`
- `term_category`
- `usage_context`
- `is_ironic`

## Final Files

- [2010_tweets_slang_analysis_ready.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_ready.csv)
- [2010_terms_annotation_table.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_terms_annotation_table.csv)
- [2010_term_origin_platform_research.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_term_origin_platform_research.csv)
