import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '7343027640',
    '7344096237',
    '7354190879',
    '7403283836',
    '7405682049',
    '7407517610',
    '7623645035',
    '7623693741',
    '8468551478',
    '8469364096',
    '9610341899',
    '9610482808',
    '7535906971',
    '7535908191',
    '8048278819',
    '8048305852',
    '13623819914',
    '13924502679',
    '14143061648',
    '7396929302',
    '8878328190',
    '9215199517',
    '10114457273',
    '10117846313',
    '12066443698',
    '12244194459',
    '10781532144',
    '13524489258',
    '14057619513',
    '14207018753',
    '19029749481',
    '20266918970',
    '21784436475',
    '22084469180',
    '7305049513',
    '7307767639',
    '7313134722',
    '7320787942',
    '7325542046',
    '7737118641',
    '7839692162',
    '7839770331',
    '7399386092',
    '7639832255',
    '8142378851',
    '11953714384',
    '7762281697',
    '7427752806',
    '11447207762',
    '8774115848',
    '8189780970',
    '8640220605',
    '7419572739',
}

drop_ids = {
    '7380695963',
    '9667110168',
    '7968647363',
    '7969106253',
    '7969106612',
    '8065197370',
    '9006489694',
    '9056585289',
    '9056683356',
    '13053035231',
    '13213097846116352',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'fashion_beauty':
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
    elif word == 'duckface':
        keep = 'http://' not in t or t.strip() == 'duckface'
    elif word == 'styling':
        keep = not any(x in t for x in ['http://', 'hair styling products', 'discount at'])
    elif word == 'wang':
        keep = False
    elif word == 'booty':
        keep = 'booty pop' in t or 'booty up' in t
    elif word == 'threads':
        keep = 'new threads' in t or 'threads..about clothes' in t
    elif word == 'bling':
        keep = not any(x in t for x in ['http://', 'bling daily', 'diamond jewelry', 'tennis bracelet'])
    elif word == 'zories':
        keep = True
    elif word == 'prettyful':
        keep = True
    elif word == 'locks':
        keep = 'locks of hair' not in t and 'http://' not in t
    elif word == 'Brotox':
        keep = True
    elif word == 'colitas':
        keep = True
    elif word == 'tenner':
        keep = True
    elif word == 'glitterati':
        keep = True
    elif word in {'chones', 'gunt', 'bomb', 'next-level', 'fanboy', 'pecker', 'sesh'}:
        keep = True
    else:
        keep = any(x in t for x in ['duckface', 'styling', 'booty', 'threads', 'zories', 'prettyful', 'locks', 'bling'])

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
