# Slang Data Cleaning And Acquisition Summary

## Project Goal

This project compares two slang datasets across time:

- a 2020-2025 Gen-Z slang dataset
- a 2010 Twitter slang dataset

The main challenge was that the Gen-Z dataset already contained richer annotation fields, while the 2010 dataset was much noisier and lacked several attributes needed for comparison. The work therefore focused on:

1. cleaning the 2010 Twitter dataset
2. extracting reusable reference vocabularies from the Gen-Z dataset
3. building a term-level annotation layer for the 2010 slang terms
4. building a tweet-level annotation layer for the 2010 rows
5. filtering out 2010 rows where the target word was not really being used as slang
6. exporting a final analysis-ready 2010 dataset

## Source Files

Primary input files:

- [2010_tweets_slang.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang.csv)
- [genz_slang_usage_2020_2025.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_slang_usage_2020_2025.csv)

Key working and output files produced during the project:

- [2010_tweets_slang_cleaned.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_cleaned.csv)
- [2010_terms_annotation_table.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_terms_annotation_table.csv)
- [2010_term_origin_platform_research.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_term_origin_platform_research.csv)
- [2010_tweets_slang_annotated.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_annotated.csv)
- [2010_tweets_slang_usage_context_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_usage_context_working.csv)
- [2010_tweets_slang_filtering_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_filtering_working.csv)
- [2010_tweets_slang_analysis_filtered.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_filtered.csv)
- [2010_tweets_slang_analysis_ready.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_ready.csv)

Reference outputs from the Gen-Z dataset:

- [genz_term_lookup.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_lookup.csv)
- [genz_term_categories.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_categories.txt)
- [genz_usage_contexts.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_usage_contexts.txt)

## 1. Initial Review And Method Decisions

The first step was reviewing the planning note and both datasets together.

The main decisions established early were:

- `term_category` should be treated as a term-level property, fixed per word
- `usage_context` should be treated as a tweet/post-level property
- the Gen-Z dataset should be used as a taxonomy reference rather than as a direct lookup source
- parity with the Gen-Z dataset should be pursued where it was methodologically defensible, but not forced

We also agreed that if a 2010 term did not fit the Gen-Z categories well, it was acceptable to create a small number of new values rather than forcing a weak match.

## 2. Cleaning The 2010 Twitter Dataset

The raw 2010 CSV contained structural problems:

- malformed header fields
- extra unnamed columns
- junk numeric rows with missing tweet metadata
- date split across separate `year`, `month`, and `day` columns

Cleaning steps:

- standardized the schema
- removed malformed junk rows
- normalized numeric-looking identifiers
- consolidated `year`, `month`, and `day` into one `date` column

Outputs:

- [2010_tweets_slang_cleaned.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_cleaned.csv)
- [clean_2010_tweets.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/clean_2010_tweets.py)

Final cleaned schema:

- `word`
- `id`
- `date`
- `text`
- `author_id`

Key result:

- 57,345 usable 2010 tweet rows were preserved after cleaning

## 3. Extracting Gen-Z Reference Sets

To make the 2010 annotations more consistent, three reference sets were extracted from the Gen-Z dataset:

1. unique `(slang_term, term_category, term_meaning)`
2. unique `term_category` values
3. unique `usage_context` values

Outputs:

- [genz_term_lookup.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_lookup.csv)
- [genz_term_categories.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_categories.txt)
- [genz_usage_contexts.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_usage_contexts.txt)
- [extract_genz_reference_sets.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/extract_genz_reference_sets.py)

Key result:

- 46 unique term rows in the lookup table
- 17 Gen-Z `term_category` values
- 17 Gen-Z `usage_context` values

## 4. Building The 2010 Term Annotation Table

A unique-word table was created from the cleaned 2010 dataset to support term-level annotation.

Output:

- [2010_terms_annotation_table.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_terms_annotation_table.csv)
- [create_2010_term_table.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/create_2010_term_table.py)

Initial columns:

- `word`
- `tweet_count`
- `first_date`
- `last_date`
- `term_meaning`
- `term_category`
- `origin_platform`
- `origin_platform_confidence`
- `notes`

Key result:

- 152 unique 2010 slang terms

## 5. Annotating 2010 Term Meaning And Term Category

We then annotated all 152 2010 terms with:

- `term_meaning`
- `term_category`

Method:

- dictionary/slang references first
- tweet samples used only to confirm or disambiguate when necessary
- Gen-Z category values reused when they fit
- new category values introduced when needed rather than forcing a weak fit

Important methodological rules agreed during annotation:

- `term_category` must stay fixed for each term
- tweet evidence can help disambiguate meaning, but does not justify multiple term categories for the same word
- acronym meanings should begin with the quoted full expansion

### Human-In-The-Loop And Subagent Review Process

The term-level annotation process was not done as a one-pass automatic labeling task. It used a layered review workflow:

1. candidate definitions and categories were researched first
2. ambiguous or borderline terms were checked against tweet evidence only as needed
3. additional review was delegated to subagents for independent judgment on difficult cases
4. proposed term batches were then shown to the user for manual review before final write-in
5. user feedback was incorporated before the approved annotations were officially added to the term table

This mattered because many terms were semantically unstable, polysemous, dated, or culturally shifted between 2010 and today. The user’s review functioned as a final approval layer, especially for cases where:

- the definition needed to be broadened or narrowed
- a Gen-Z-aligned category fit was uncertain
- the wording of `term_meaning` needed to be made clearer
- acronym formatting needed to be standardized

Examples of terms whose final annotation changed through this review process include:

- `gnarly`
- `badass`
- `AWOL`
- `BFFL`
- `twit`
- `gag`
- `God`
- `fap`
- `thirsty`
- `gangsta`

This means the final term table was produced through a collaborative, iterative annotation workflow rather than a single-model automatic pass.

Examples of category alignment and revision:

- `CBA` was fixed as `behavior`
- `gnarly` was broadened to include both negative and positive/intense uses, while staying `description`
- `gangsta` was made to exactly match `gansta`
- `twit` was revised to mean shorthand for `Twitter`

New term-category values added when needed:

- `money`
- `technology`
- `religion`
- `animals`
- `sex`

Batch scripts were created throughout this process:

- [apply_2010_term_annotations_batch1.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/apply_2010_term_annotations_batch1.py)
- through
- [apply_2010_term_annotations_batch16.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/apply_2010_term_annotations_batch16.py)

Key result:

- all 152 terms received a `term_meaning`
- all 152 terms received a fixed `term_category`

## 6. Propagating Term-Level Annotations Back To Tweet Rows

After term-level annotation was complete, the term annotations were merged back into the row-level 2010 tweet dataset.

Output:

- [2010_tweets_slang_annotated.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_annotated.csv)
- [annotate_2010_tweets_with_terms.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/annotate_2010_tweets_with_terms.py)

Appended columns:

- `term_meaning`
- `term_category`

Key result:

- all 57,345 cleaned rows received both term-level fields

## 7. Building A 2010 Usage Context / Irony Annotation Workflow

Next, tweet-level annotation fields were added to make the 2010 dataset more structurally comparable to the Gen-Z dataset.

Working file:

- [2010_tweets_slang_usage_context_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_usage_context_working.csv)

Working columns:

- `usage_context`
- `is_ironic`
- `annotation_notes`

Guidelines file:

- [2010_usage_context_annotation_guide.md](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_usage_context_annotation_guide.md)

We first examined how the Gen-Z `usage_context` field behaved and concluded that it functioned as a broader post/tweet context rather than as a narrow local-sense label for the target word. Based on that, the 2010 annotation followed a tweet/post-context interpretation.

Additional context labels were introduced when the Gen-Z set was not sufficient, including:

- `article_sharing`
- `sports_discussion`
- `technology_discussion`
- `sexual_context`
- `drug_context`
- `book_discussion`
- `television_reference`

### Review Workflow For Usage Context

A multi-agent review workflow was used:

- Euler, Kant, and Kuhn reviewed the active category
- Darwin trailed the previous category
- Cicero audited `is_ironic` decisions across batches

This workflow was used category-by-category across the full tweet set.

The same basic philosophy from term-level annotation carried over here as well:

- one pass to generate an initial working classification
- independent review on the active batch
- trailing audit on the previous batch
- then consolidation into the final working file

### Usage Context Categories Completed

All tweet rows were annotated across the full 2010 dataset for:

- `usage_context`
- `is_ironic`

Key result:

- 57,345 / 57,345 rows received `usage_context`
- 57,345 / 57,345 rows received valid `is_ironic`

## 8. Researching Origin Platform For 2010 Terms

After term meaning/category work was complete, the term table was extended with:

- `origin_platform`
- `origin_platform_confidence`

This required historical slang-origin research using a mix of:

- Know Your Meme
- Urban Dictionary
- Wiktionary
- Merriam-Webster
- Green’s Dictionary of Slang
- Dictionary.com
- other origin/etymology references where needed

A separate provenance table was created to record:

- source link
- confidence
- short reasoning note

Outputs:

- [2010_term_origin_platform_research.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_term_origin_platform_research.csv)
- [apply_origin_platform_batch1.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/apply_origin_platform_batch1.py)
- later origin batches were applied directly into the research/annotation files during the process

Allowed origin labels ultimately included:

- `offline_general_slang`
- `instant_messaging_texting`
- `internet_forums`
- `twitter`
- `youtube`
- `gaming`
- `music_hiphop`
- `printed_literature`
- `television_film`

Key result:

- all 152 terms received `origin_platform`
- all 152 terms received `origin_platform_confidence`
- all 152 terms received a source/note row in the research CSV

## 9. Designing And Applying Row-Level Slang Filtering

After the annotation layers were complete, we introduced a second-stage filtering process to remove rows where the tweet contained the target token but was not really using it as slang in a useful analytic sense.

This required a separate filtering workflow because a row could have a valid `usage_context` but still be analytically weak for slang-use comparison.

Working file:

- [2010_tweets_slang_filtering_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_filtering_working.csv)

Added columns:

- `keep_for_slang_analysis`
- `exclusion_reason`

Workflow documentation:

- [2010_row_filtering_rules.md](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_row_filtering_rules.md)
- [2010_row_filtering_workflow.md](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_row_filtering_workflow.md)

### Review Workflow For Filtering

The filtering workflow reused the multi-agent pattern:

- active review: Euler, Kant, Kuhn
- trailing review: Darwin, Cicero

The rule was not simply “drop by context.” Instead:

- `usage_context` was used as triage
- rows were then reviewed in terms of whether the target word was actually being used as slang/informal lexical material

This filtering stage also remained human-guided throughout. Several times the user clarified important methodological preferences that changed the filtering logic, for example:

- keep domain-specific jargon when it is still functioning as slang or informal lexical material
- keep metalinguistic discussion of slang terms
- keep some short semantic invocations even when they overlap with media/title language
- avoid dropping rows just because they occur in a specific topical domain

### Contexts Reviewed In Filtering

Filtering passes were completed for all `usage_context` groups, including:

- `advertising_spam`
- `article_sharing`
- `music_discussion`
- `technology_discussion`
- `television_reference`
- `sports_discussion`
- `book_discussion`
- `gaming`
- `news_reaction`
- `fashion_beauty`
- `celebrity_gossip`
- `commenting`
- `casual_conversation`
- `self_description`
- `reaction`
- `humor`
- `compliment`
- `criticism`
- `food_related`
- `sexual_context`
- `work_school`
- `storytelling`
- `drug_context`
- `religion`
- `meme_reference`
- `dating_context`

The filtering script set grew into a full numbered series:

- [filter_round1_advertising_spam.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/filter_round1_advertising_spam.py)
- through
- [filter_round28_dating_context.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/filter_round28_dating_context.py)

### Important Filtering Principles Established

- keep domain-specific slang/jargon if the target word is still functioning informally
- keep metalinguistic slang discussion like “what is a sploof”
- keep short semantic invocations even if they overlap with media/title phrases, as long as the author is still actually using the slang term
- drop pure title, product, handle, file-format, article-shell, or promo-shell noise
- drop literal non-slang senses when they no longer matched the intended slang meaning

### Technical Note On Rebuilds

During filtering, the working CSV briefly became inconsistent due to sequential replay and partial corruption. To make the process reproducible and stable, the filtering working file could be rebuilt from the fully annotated usage-context file using:

- [create_2010_filtering_working_file.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/create_2010_filtering_working_file.py)

### Final Filtering Result

Key result:

- 35,987 rows kept for slang analysis
- 21,327 rows excluded
- 0 rows left unreviewed

## 10. Exporting The Final Filtered And Analysis-Ready 2010 Datasets

After the row-level filtering was completed, two final exports were produced.

### Full Filtered Export

This retains the filtering helper columns:

- [2010_tweets_slang_analysis_filtered.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_filtered.csv)
- [export_filtered_2010_analysis_dataset.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/export_filtered_2010_analysis_dataset.py)

Columns:

- `word`
- `id`
- `date`
- `text`
- `author_id`
- `term_meaning`
- `term_category`
- `usage_context`
- `is_ironic`
- `annotation_notes`
- `keep_for_slang_analysis`
- `exclusion_reason`

### Clean Analysis-Ready Export

This removes the filtering helper columns and keeps only analysis-relevant fields:

- [2010_tweets_slang_analysis_ready.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_ready.csv)
- [export_filtered_2010_analysis_ready_dataset.py](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/scripts/export_filtered_2010_analysis_ready_dataset.py)

Final columns:

- `word`
- `id`
- `date`
- `text`
- `author_id`
- `term_meaning`
- `term_category`
- `usage_context`
- `is_ironic`

Key result:

- 36,005 rows in the final analysis-ready 2010 dataset

## Final Deliverables Produced

### Cleaned 2010 data

- [2010_tweets_slang_cleaned.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_cleaned.csv)

### 2010 term-level resources

- [2010_terms_annotation_table.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_terms_annotation_table.csv)
- [2010_term_origin_platform_research.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_term_origin_platform_research.csv)

### 2010 row-level annotated resources

- [2010_tweets_slang_annotated.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_annotated.csv)
- [2010_tweets_slang_usage_context_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_usage_context_working.csv)
- [2010_tweets_slang_filtering_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_filtering_working.csv)

### Final filtered analysis datasets

- [2010_tweets_slang_analysis_filtered.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_filtered.csv)
- [2010_tweets_slang_analysis_ready.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_analysis_ready.csv)

### Gen-Z reference resources

- [genz_term_lookup.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_lookup.csv)
- [genz_term_categories.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_term_categories.txt)
- [genz_usage_contexts.txt](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/genz_usage_contexts.txt)

## Final State Of The 2010 Dataset

The final 2010 analysis-ready file now contains:

- cleaned row structure
- one unified `date` field
- fully populated `term_meaning`
- fully populated `term_category`
- fully populated `usage_context`
- fully populated `is_ironic`
- row-level slang-use filtering already applied

In other words, the 2010 dataset has been transformed from a noisy raw slang-token file into a structured comparative dataset that is much closer to the Gen-Z dataset in analytical usefulness.
