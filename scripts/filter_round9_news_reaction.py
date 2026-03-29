import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '9726852601',
    '15818566979',
    '16258359944',
    '16258383614',
    '19355869720354816',
    '10958186063',
    '10958264624',
    '12573531459',
    '20874239774',
    '7486119021',
    '7487899756',
    '9736306895',
    '9066247191',
    '20151976609',
    '17305487309',
}

drop_ids = {
    '9235786765',
    '9768959970',
    '10606172071',
    '8469749497',
    '11910162093',
    '9591361942',
    '10334585147',
    '7980429124',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'news_reaction':
        continue

    text = row['text'] or ''
    t = text.lower()
    keep = False
    reason = 'title_or_media_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif row['word'] == 'bomb':
        keep = 'bomb scare' in t or 'bomb threat' in t or 'debt bomb' in t or 'explosive' in t
    elif row['word'] == 'meme':
        keep = True
    elif row['word'] == 'money':
        keep = 'follow the money' in t
    elif row['word'] == 'gridlock':
        keep = True
    elif row['word'] == 'skyrocket':
        keep = True
    elif row['word'] == 'dang':
        keep = True
    elif row['word'] == 'bible-thumping':
        keep = True
    elif row['word'] in {'relly', 'dafuq'}:
        keep = True
    elif row['word'] in {'bling', 'rehab', 'hells', 'KMT', 'blowjob', 'fire'}:
        keep = False
    else:
        keep = any(
            x in t for x in ['dang ', 'dafuq', 'meme', 'skyrocket', 'gridlock', 'bomb scare', 'bomb threat']
        )

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
