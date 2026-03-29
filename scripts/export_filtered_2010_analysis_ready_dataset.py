import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
source = root / '2010_tweets_slang_analysis_filtered.csv'
target = root / '2010_tweets_slang_analysis_ready.csv'

keep_columns = [
    'word',
    'id',
    'date',
    'text',
    'author_id',
    'term_meaning',
    'term_category',
    'usage_context',
    'is_ironic',
]

with source.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

cleaned = [{column: row[column] for column in keep_columns} for row in rows]

with target.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=keep_columns)
    writer.writeheader()
    writer.writerows(cleaned)

print(f'Wrote {len(cleaned)} rows to {target}')
