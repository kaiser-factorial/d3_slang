# 2010 Row Filtering Workflow

## Objective

Create a cleaned 2010 tweet dataset that keeps rows where the target `word` is actually used as slang and removes rows where the word is only present as noise, title, name, product, or non-slang literal usage.

## Working File

Use:

- `2010_tweets_slang_filtering_working.csv`

Key columns for filtering:

- `keep_for_slang_analysis`
- `exclusion_reason`

## Review Workflow

### Active batch review

For the active batch:

- `Euler`
- `Kant`
- `Kuhn`

Each reviews the same active section independently.

Then the main thread reconciles the result.

### Trailing audit

Starting in round 2:

- `Darwin`
- `Cicero`

These two review the previous round while the active round is being processed.

## Batch Order

Recommended filtering order:

1. `advertising_spam`
2. `article_sharing`
3. `music_discussion`
4. `technology_discussion`
5. `television_reference`
6. `sports_discussion`
7. `book_discussion`
8. `gaming`
9. term-specific cleanup for especially noisy words

## Default Actions

### `advertising_spam`

Default bias: exclude.

Keep only if the tweet clearly uses the target word as slang in the tweet text itself and the word is not just part of a title, brand, listing, promo, or link.

### Review-heavy contexts

For these, inspect row meaning:

- `article_sharing`
- `music_discussion`
- `technology_discussion`
- `television_reference`
- `sports_discussion`
- `book_discussion`
- `gaming`

Keep if the tweet actively uses the word as slang.

Exclude if the word is mainly:

- a title
- a proper name
- a product or model
- a media reference
- a technical file/software term
- a headline keyword

## Exclusion Reasons

Use one of:

- `advertising_or_spam`
- `proper_name_or_handle`
- `title_or_media_reference`
- `product_or_technical_reference`
- `literal_non_slang_use`
- `meta_word_reference`
- `unclear_borderline`

## Output Goal

After review, each processed row should have:

- `keep_for_slang_analysis = true` or `false`
- `exclusion_reason` filled only when `false`
