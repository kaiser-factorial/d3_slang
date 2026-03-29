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
    '11356796747',
    '11678051482',
    '12632168904',
    '12632275784',
    '14572347253',
    '27434949703',
    '25665326436',
    '7937956988',
    '8293131273',
    '10271891588',
    '11740097529',
    '8564860166',
    '12595976522',
    '9233377702',
    '9827419030',
    '8349430296',
    '2273568205316096',
    '12194290260',
    '18048935361',
    '11032070423842816',
    '20539876407',
}

keep_ids = {
    '7713907729',
    '8569503091',
    '8569755449',
}

for row in rows:
    if row['id'] in keep_ids:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''
    elif row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'title_or_link_shell'

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
