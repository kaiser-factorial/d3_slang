import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    row.pop(None, None)

fieldnames = list(rows[0].keys())

keep_ids = {
    '11401696960',  # looked kosher today
    '13215477862',  # you're so kosher
    '16765984013',  # jewPhone / Kosher? Bet your Yarmulke!
    '16765556916',  # kosher salt wordplay
}

drop_ids = {
    '8362757326',
    '8867020735',
    '8867178656',
    '9572477630',
    '11328409063',
    '11328505803',
    '11328652540',
    '11328728369',
    '11328741923',
    '11401721659',
    '11401974141',
    '11651691490',
    '11651767149',
    '11651790835',
    '11652057176',
    '12404600083',
    '16764946932',
    '17392374611',
    '18268772593',
    '18469162272',
    '20703836183',
    '29175865140',
    '29176002382',
    '10125454623117312',
    '10125935319711744',
    '20632389994',
}

for row in rows:
    if row['usage_context'] != 'religion':
        continue

    if row['id'] in keep_ids:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''
    elif row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'literal_or_title_reference'
    else:
        # Conservative default: religion bucket is mostly literal/non-slang.
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'literal_or_title_reference'

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
