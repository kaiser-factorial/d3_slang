import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

drop_ids = {
    '7337472320',  # account notice, not peeps slang
    '7375609231',  # by Mozzie signoff/name
    '7994787365',  # named Skeeter
    '8570963117',  # pet/name Skeeter
    '9233377702',  # Skeeter handle
    '9680857541',  # Skeeter handle/name
    '9826254724',  # Skeeter signoff
}

for row in rows:
    if row['usage_context'] != 'casual_conversation':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'proper_name_or_team_reference'

    if row['id'] in drop_ids:
        keep = False
    elif word in {'sis', 'bro', 'lemme', 'peeps', 'BFFL', 'dis', 'sesh', 'F2F', 'wut', 'whadja', 'dudette', 'lowkey', 'twit', 'dogg'}:
        keep = True
    elif word == 'freckle':
        keep = '@freckle_' not in t and '@freckle' not in t
    elif word == 'pedo':
        keep = not any(x in t for x in [' que pedo', 'qué pedo', 'pedo oppa', ' pedo unni'])
    elif word == 'ent':
        keep = any(x in t for x in [" i ent ", " ent got ", " ent coming ", " ent album like ", " ain't"]) and not any(
            x in t for x in ['_ent', '@365_ent', 'crimesquare_ent', 'cb_ent']
        )
    elif word == 'skeeter':
        keep = any(x in t for x in ['skeeter-sucked', 'skeeter sucked', 'call me skeeter', 'upset skeeter']) and not any(
            x in t for x in ['@skeeter', ' skeeterhansen', 'named skeeter', "playing with skeeter", "skeeter's fart"]
        )
    elif word == 'mozzie':
        keep = 'mozzie sticks' not in t and 'by mozzie' not in t and 'what is a mozzie' in t or 'mozzie?' in t or 'whats a mozzie' in t
    elif word == 'walkie':
        keep = not any(x in t for x in ['go walkie', 'for walkie', 'walkies'])
    elif word == 'colitas':
        keep = any(x in t for x in [' colitas ', 'two colitas', '2 colitas', '3 colitas'])
    elif word == 'pecker':
        keep = not any(x in t for x in ['wood pecker', 'woodpecker', '@pecker'])
    elif word == 'wang':
        keep = any(x in t for x in ['pulling my wang', 'love you bitches. and wang', 'wang bang'])
    elif word == 'jill':
        keep = False
    elif word == 'sport':
        keep = any(x in t for x in ['good sport', 'spoil sport', 'sport these'])
    elif word == 'money':
        keep = True
    elif word in {'crappy', 'thirsty', 'poopy', 'fire', 'gnarly', 'gangsta', 'gansta', 'shiesty', 'sicc', 'whooty', 'rad', 'zooted', 'lame-o', 'okee-doke', 'revert', 'gag', 'bumfuck', 'roofie', 'compy', 'workaround', 'gunt', 'locks'}:
        keep = True
    else:
        keep = not any(x in t for x in ['http://', 'https://', 'rt @', 'follow me', 'follow @'])

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
