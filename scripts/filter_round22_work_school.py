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
    '8232404128',  # compy
    '9682765077',  # dis
    '12514747813', # rachet
    '7334416702',  # GLHF
    '8767220403',  # chillax
    '19349353640', # dafuq
    '7337499293',  # peeps
    '7394282022',  # sesh
    '7344341725',  # sis
}

drop_ids = {
    '7422357969',  # TOEFL iBT
    '8065593982',  # rehab job listing
    '7516545080',  # F2F admin shorthand
    '7695184894',  # F2F article/academic shorthand
    '17904985280', # Money Matters title shell
    '7361257662',  # revert admin
    '7362462900',
    '7436219157',
    '7798476591',  # thingamabob title shell
    '28920811605', # thingamabob title/media ref
    '7713907729',  # blumpkin metalinguistic mention
    '8065754689',  # rehab professional listing
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'work_school':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'institutional_or_title_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word == 'IBT':
        keep = False
        reason = 'institutional_or_title_reference'
    elif word == 'rehab':
        keep = not has_any(t, ['job', 'career', 'therapist', 'rehabilitation services', 'professional rehab'])
        reason = 'institutional_or_title_reference'
    elif word == 'BFFL':
        keep = True
    elif word == 'F2F':
        keep = not has_any(t, ['therapy', 'clinical', 'article', 'study', 'conference'])
        reason = 'institutional_or_title_reference'
    elif word == 'compy':
        keep = True
    elif word == 'dis':
        keep = True
    elif word == 'sinse':
        keep = True
    elif word == 'rachet':
        keep = True
    elif word == 'money':
        keep = not has_any(t, ['money matters', 'finance office', 'tuition money'])
        reason = 'institutional_or_title_reference'
    elif word == 'GLHF':
        keep = True
    elif word == 'chillax':
        keep = True
    elif word == 'revert':
        keep = not has_any(t, ['revert me back', 'pls email us', 'care@', 'ask@', 'budget/requirement'])
        reason = 'institutional_or_title_reference'
    elif word == 'thingamabob':
        keep = False
        reason = 'institutional_or_title_reference'
    elif word in {'dafuq', 'blumpkin', 'peeps', 'sesh', 'sis', 'booty', 'bupkis', 'hells', 'shart', 'wut', 'ent', 'okee-doke'}:
        keep = True
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
