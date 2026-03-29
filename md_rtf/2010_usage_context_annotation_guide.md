# 2010 Tweet-Level Annotation Guide

This guide is for annotating tweet-level `usage_context` and `is_ironic` in [2010_tweets_slang_usage_context_working.csv](/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj/2010_tweets_slang_usage_context_working.csv).

## Goal

Annotate each tweet for:
- `usage_context`: the main communicative context of the tweet
- `is_ironic`: whether the tweet is clearly ironic, sarcastic, mock-serious, or deliberately nonliteral

`term_meaning` and `term_category` are already fixed at the word level. These new fields are tweet-level and can vary row by row.

## Core Rule

Choose the tweet's main function, not just the slang word's meaning.

Examples:
- A tweet containing an insult word can still be `humor` if it is clearly a joke.
- A tweet containing a reaction word can still be `storytelling` if it is mainly narrating an event.

## Preferred Usage Context Labels

Use these Gen-Z labels when they fit:
- `casual_conversation`
- `celebrity_gossip`
- `commenting`
- `compliment`
- `criticism`
- `dating_context`
- `fashion_beauty`
- `food_related`
- `gaming`
- `humor`
- `meme_reference`
- `music_discussion`
- `news_reaction`
- `reaction`
- `self_description`
- `storytelling`
- `work_school`

Use these additional 2010 labels when needed:
- `sports_discussion`
- `technology_discussion`
- `book_discussion`
- `television_reference`
- `sexual_context`
- `drug_context`
- `article_sharing`
- `advertising_spam`

## Label Rules

### `casual_conversation`
Use for ordinary interpersonal chat, check-ins, replies, and low-stakes back-and-forth.

### `celebrity_gossip`
Use for discussion of celebrities, public figures, fame, tabloids, or celebrity behavior.

### `commenting`
Use for general opinions, observations, or remarks when no sharper label fits better.

### `compliment`
Use when the tweet is clearly praising a person, thing, performance, or appearance.

### `criticism`
Use when the tweet is clearly attacking, disapproving of, or negatively evaluating a target.

### `dating_context`
Use for romance, flirting, partners, crushes, breakup talk, or dating situations.

### `fashion_beauty`
Use for makeup, hair, clothes, style, beauty routines, or physical presentation.

### `food_related`
Use when the tweet is mainly about eating, cooking, meals, snacks, or food preferences.

### `gaming`
Use for video games, gameplay, consoles, co-op, DLC, online matches, and game culture.

### `humor`
Use for clear jokes, punchlines, playful absurdity, or comic framing.

### `meme_reference`
Use when the tweet is mainly invoking an internet meme, recurring quote, or recognizable meme format.

### `music_discussion`
Use for songs, artists, lyrics, albums, radio play, concerts, or music opinions.

### `news_reaction`
Use when reacting to a current event, reported story, or news item.

### `reaction`
Use for brief emotional outbursts, exclamations, disbelief, disgust, surprise, or frustration.

### `self_description`
Use when the speaker is describing their own state, mood, identity, behavior, or condition.

### `storytelling`
Use when the tweet mainly narrates an event, sequence, or anecdote.

### `work_school`
Use for jobs, homework, class, assignments, teachers, studying, office life, or school obligations.

### `sports_discussion`
Use for games, teams, scores, athletes, leagues, or sports events.

### `technology_discussion`
Use for software, devices, files, internet tools, digital formats, online platforms, or tech troubleshooting.

### `book_discussion`
Use for novels, authors, literary genres, reading habits, publishing, book reviews, covers, or discussion of a work as a book/genre object.

### `television_reference`
Use for TV shows, TV characters, episodes, broadcast nostalgia, or discussion of a work as a television reference.

### `sexual_context`
Use for sexual acts, sexual body references, erotic framing, horniness, or explicit sexual discussion.

### `drug_context`
Use for intoxication, weed, drugs, drug paraphernalia, or drug-related references.

### `article_sharing`
Use for one-off sharing of a news article, blog post, interview, essay, or linked writeup when the post is mainly passing along that content rather than reacting strongly to it.

### `advertising_spam`
Use for obvious promotion, link-blasting, auto-posts, repetitive marketing, or commercial spam.

## Choosing Between Similar Labels

- `reaction` vs `commenting`:
  Use `reaction` for short affective responses. Use `commenting` for fuller observations or opinions.

- `self_description` vs `storytelling`:
  Use `self_description` for current state. Use `storytelling` when recounting what happened.

- `criticism` vs `humor`:
  If the main force is condemnation, use `criticism`. If the main force is joking, use `humor`.

- `technology_discussion` vs `advertising_spam`:
  If the tweet is genuinely discussing tech, use `technology_discussion`. If it is just promoting a product or posting a link repeatedly, use `advertising_spam`.

- `article_sharing` vs `advertising_spam`:
  Use `article_sharing` for ordinary sharing of an article or writeup. Use `advertising_spam` only for obvious promo, repetitive blasts, or marketing-like posting.

## `is_ironic` Rules

Mark `is_ironic = true` only when irony is clear.

Set `true` when the tweet is:
- sarcastic
- mock-serious
- clearly opposite-to-literal
- knowingly exaggerated for comic effect
- using a slang term in a playful, nonliteral, or self-aware way

Set `false` when the tweet is:
- sincere
- literal
- straightforward
- ambiguous about irony

When uncertain, default to `false` and explain only if needed in `annotation_notes`.

## `annotation_notes`

Use notes only when:
- the tweet could plausibly take two labels
- irony is ambiguous
- the tweet is noisy, spammy, or semantically weak
- the term meaning itself is not the main issue, but the context is messy

Keep notes short.
