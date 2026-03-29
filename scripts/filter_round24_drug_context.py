import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    row.pop(None, None)

fieldnames = list(rows[0].keys())

drop_ids = {
    '28396784702',  # Hotel California lyric reference
}

for row in rows:
    if row['usage_context'] != 'drug_context':
        continue

    if row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'title_or_lyric_reference'
    else:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
