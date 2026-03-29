import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
source = root / '2010_tweets_slang_filtering_working.csv'
target = root / '2010_tweets_slang_analysis_filtered.csv'

with source.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    row.pop(None, None)

filtered = [row for row in rows if row['keep_for_slang_analysis'] == 'true']

fieldnames = list(filtered[0].keys())

with target.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered)

print(f'Wrote {len(filtered)} rows to {target}')
