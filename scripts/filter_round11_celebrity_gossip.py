import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '7394718929',
    '9915455423',
    '12371101981',
    '12371522519',
    '12374139165',
    '9901998112',
    '10288609144',
    '10432871388',
    '12935003163',
    '14638561262',
    '14641067845',
    '7901168257',
    '12551670200',
    '18843628610',
    '8065589419',
    '9490644081',
    '9966900448',
    '14697729477',
    '23007497454',
    '5596209712467968',
    '7310798888',
    '10180550653',
    '10180865439',
    '10858962688',
    '18898824638',
    '18899094283',
    '22582175525',
    '11848332724928512',
    '18476821820',
    '26145823824',
    '7601840928',
    '8058200832',
    '8058591685',
    '8061916606',
    '15604458037',
    '19429549870',
    '8003514951',
    '8004833323',
    '7507612931',
    '7507770951',
    '7600932080',
    '7539851910',
    '7361488669',
    '14459217020',
    '7615020825',
}

drop_ids = {
    '7394823705',
    '9837955473',
    '11537324447',
    '8893202056',
    '15758721839',
    '8941307433',
    '9142307720',
    '9145373292',
    '18558622440',
    '8065650716',
    '8065661235',
    '18473835926',
    '18476620834',
    '18476644548',
    '18483836571',
    '26158063370',
    '15332978877',
    '16321870440',
    '19556587259',
    '8404572160',
    '8592307875',
    '24308467184',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'celebrity_gossip':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = False
    reason = 'title_or_media_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word == 'a-list':
        keep = 'a-list' in t and 'http://' not in t
    elif word == 'bling':
        keep = 'spring bling' in t or 'bling!' in t
    elif word == 'glitterati':
        keep = True
    elif word == 'celebutante':
        keep = 'http://' not in t and 'socialite' not in t
    elif word == 'rehab':
        keep = 'celeb rehab' in t or 'send' in t or 'lmao' in t or 'rehab help' in t
    elif word == 'BFFL':
        keep = True
    elif word == 'bonehead':
        keep = 'bonehead' in t and 'http://' not in t
    elif word == 'shtick':
        keep = True
    elif word == 'money':
        keep = False
    elif word == 'Brotox':
        keep = True
    elif word in {'bromance', 'motherfucking', 'lame-o', 'slore', 'dafuq', 'sis'}:
        keep = True
    else:
        keep = any(x in t for x in ['a-list', 'bffl', 'shtick', 'bromance', 'brotox', 'dafuq', 'rehab', 'bonehead'])

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
