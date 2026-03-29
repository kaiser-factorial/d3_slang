# Abstract-Style Summary

To compare a 2020-2025 Gen-Z slang dataset with a 2010 Twitter slang dataset, the 2010 data first had to be transformed into a more comparable analytical structure. The raw 2010 dataset was cleaned by fixing malformed columns, removing junk rows, and consolidating separate year/month/day fields into a single `date` field. Reference vocabularies were then extracted from the Gen-Z dataset to guide annotation.

Next, all unique 2010 slang terms were annotated with fixed `term_meaning` and `term_category` values, using a combination of dictionary/slang research, targeted context checks, delegated review, and manual human approval. Tweet-level attributes were then added to the 2010 data, including `usage_context` and `is_ironic`, using a category-by-category annotation workflow with multiple layers of review.

The 2010 term table was further enriched with `origin_platform` and `origin_platform_confidence`, supported by a separate provenance table documenting sources and notes. Finally, a row-level filtering stage removed tweets in which the target token appeared but was not meaningfully functioning as slang. This yielded a final filtered 2010 analysis-ready dataset of 36,005 rows with the fields `word`, `id`, `date`, `text`, `author_id`, `term_meaning`, `term_category`, `usage_context`, and `is_ironic`.
