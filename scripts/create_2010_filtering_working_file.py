import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / '2010_tweets_slang_usage_context_working.csv'
OUTPUT_PATH = ROOT / '2010_tweets_slang_filtering_working.csv'


with SOURCE_PATH.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())
for column in ['keep_for_slang_analysis', 'exclusion_reason']:
    if column not in fieldnames:
        fieldnames.append(column)

for row in rows:
    row['keep_for_slang_analysis'] = ''
    row['exclusion_reason'] = ''

with OUTPUT_PATH.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Wrote {len(rows)} rows to {OUTPUT_PATH}')
