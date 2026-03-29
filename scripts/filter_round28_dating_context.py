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
    '7599403953',  # rad date
    '8284587277',  # McDreamy
    '8400153190',  # McDreamy
    '9414638241',  # whooty
    '8573109167',  # shart / date is over
    '8172303894',  # carny boy
    '12113708647', # word of the day - hasbian
    '14895303890', # ex-lesbian is called hasbian?
    '17151365969', # hasbian definition joke
    '17152374659', # hasbian/HAY wordplay
    '17152581837', # hasbian/HAY RT
    '18290343302', # meaningful hasbian discussion
    '20938855541', # hasbian = former lesbian
    '25792751874', # hasbian / wasbian question
    '9398298955751424', # called a hasbian
    '17133503565004800', # new term learned
    '19195330989920256', # definition of HASBIAN
    '9307908872',  # dang / caking time
}

drop_ids = {
    '7717315719',  # fire lyric-like romance line
    '9593267577',  # quote
    '20700073737', # RT quote
    '7686056661',  # hasbian article/link
    '7687173307',
    '7701963015',
    '7733980824',
    '7749872946',
    '7750294982',
    '7756523941',
    '11049134898',
    '7152251474808832',
    '9299598862454784',
}

for row in rows:
    if row['usage_context'] != 'dating_context':
        continue

    if row['id'] in keep_ids:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''
    elif row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'title_or_link_shell'
    else:
        # Conservative default for the few leftovers: keep direct in-body dating use.
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
