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
    '7432443048',  # badass
    '7313385385',  # prettyful
    '7752849146',  # shiznat
    '7318889565',  # rad
    '7849432693',  # bomb
    '11694414087', # fire slang praise
    '7431367338',  # DFTBA
    '7310892434',  # BFFL
    '8361280607',  # kosher
    '7333673190',  # sicc
}

drop_ids = {
    '21018573206', # month of the fire
    '21018582015', # mouth on fire
    '16087882704', # weak DFTBA signoff
    '8464624502',  # next-level progression/status
    '8464911798',
    '8582101704',
    '7472776105',  # weak kosher event description
    '8103908004',  # whooty as label
    '8612889057',  # whooty promo-like sexualized label
    '8469740598',  # promo shell around fire
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'compliment':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'literal_or_title_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word in {'badass', 'prettyful', 'shiznat', 'rad', 'bomb', 'BFFL', 'sicc', 'relly', 'duckface', 'slack-jawed', 'threads', 'skyrocket', 'dudette', 'fanboy', 'dafuq', 'dang', 'peeps'}:
        keep = True
    elif word == 'fire':
        keep = not has_any(t, ['on fire', 'shots fire', 'month of the fire', 'russia is on fire', 'dcfireems', 'pants on fire'])
        reason = 'literal_non_slang_sense'
    elif word == 'DFTBA':
        keep = not has_any(t, ['signoff only', 'auto sig'])
        reason = 'formulaic_signoff_reference'
    elif word == 'next-level':
        keep = False
        reason = 'generic_progression_phrase'
    elif word == 'kosher':
        keep = has_any(t, ['is kosher', "he's kosher", 'she is kosher'])
        reason = 'non_compliment_sense'
    elif word == 'whooty':
        keep = False
        reason = 'identity_or_sexualized_label'
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
