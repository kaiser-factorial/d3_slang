# 2010 Tweet Filtering Rules

## Goal

Keep rows where the tweet actually uses the target `word` as slang or slang-like language in context.

Remove rows where the target `word` appears, but the tweet is really about a proper name, title, product, acronym, technical file type, literal non-slang sense, or other noise.

## Core Rule

Do not filter by `usage_context` alone.

`usage_context` is a triage signal, not the final decision. A row should be kept or removed based on how the target word is functioning in that tweet.

## Keep

Keep a row when the target word is used:

- as a slang term, insult, exclamation, intensifier, identity label, reaction, or informal descriptor
- as an informal conversational variant or abbreviation that still functions like slang in context
- in a joking, ironic, or playful slang use
- in first-person, interpersonal, evaluative, or expressive language

Examples:

- `thirsty` meaning desperate for attention
- `jabroni` used to insult someone
- `wut` used as an informal reaction
- `zounds!` used as an exclamation

## Remove

Remove a row when the target word is used:

- as a proper name, username, handle, band name, store name, or organization name
- as a title of a song, album, movie, TV show, article, book, or event
- as a product, model, software format, or technical item instead of slang
- in a fully literal standard-language sense when that sense is not really slang
- only as quoted reference or meta-discussion of the word, rather than actual slang use
- as spam/promo/linkbait where the word is just part of a title or keyword

Examples:

- `streak` in `Dell Streak`
- `McDreamy` in article headlines about Grey's Anatomy, if it is just title/reference noise
- `SWF` when it clearly means the Flash file format
- `zounds` in band/event listings where it is just the band name

## Triage By Usage Context

### Strong keep candidates

These contexts are more likely to contain genuine slang use:

- `casual_conversation`
- `commenting`
- `self_description`
- `reaction`
- `humor`
- `compliment`
- `criticism`
- `dating_context`
- `drug_context`
- `sexual_context`
- `fashion_beauty`
- `food_related`
- `storytelling`

These should still be checked for literal/non-slang uses, but the default bias is keep.

### Strong drop candidates

These contexts are more likely to contain non-slang noise:

- `advertising_spam`

Default bias: drop unless the tweet very clearly uses the target word as slang in the tweet text itself.

### Review-heavy contexts

These often contain a mix of real slang and reference noise:

- `article_sharing`
- `music_discussion`
- `technology_discussion`
- `television_reference`
- `sports_discussion`
- `book_discussion`
- `gaming`
- `celebrity_gossip`
- `news_reaction`
- `work_school`
- `meme_reference`
- `religion`

For these, inspect the row and ask:

1. Is the target word being used by the tweeter as slang?
2. Or is it just the name/title/topic of the linked thing?

If it is mostly title/topic/reference, drop it.

## Decision Questions

For each row, use this order:

1. Is the target word actually being used in the tweet body, not just pasted from a title/link/name?
2. Is the usage slang/informal in context, rather than purely literal or technical?
3. If the word has both slang and non-slang senses, which sense is active here?
4. If unclear, prefer review over automatic deletion.

## Recommended Output Columns

If we create a filtered version, add:

- `keep_for_slang_analysis` = `true` or `false`
- `exclusion_reason`

Recommended `exclusion_reason` values:

- `proper_name_or_handle`
- `title_or_media_reference`
- `product_or_technical_reference`
- `literal_non_slang_use`
- `meta_word_reference`
- `advertising_or_spam`
- `unclear_borderline`

## Recommended First-Pass Filter

Safe first pass:

- auto-drop rows with `usage_context = advertising_spam`
- review rows in:
  - `article_sharing`
  - `music_discussion`
  - `technology_discussion`
  - `television_reference`
  - `sports_discussion`
  - `book_discussion`
  - `gaming`
- keep the remaining rows unless a term-specific check shows clear non-slang noise

## Practical Note

The biggest source of bad rows is not casual conversation. It is title/name/reference contamination:

- songs
- headlines
- product names
- brand names
- usernames
- app/site/service names

So the best filtering strategy is:

1. remove obvious spam
2. target the review-heavy reference contexts
3. for especially noisy words, do term-specific cleanup
