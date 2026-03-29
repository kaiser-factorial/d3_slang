import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())
keep_ids = {'7358924021', '8171228080', '8179776713'}
drop_ids = {'7746648237'}

for row in rows:
    if row['usage_context'] != 'commenting':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = False
    reason = 'literal_or_topic_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
        reason = 'title_or_media_reference'
    elif word == 'compo':
        keep = any(x in t for x in ['getting compo', 'claim compo', 'pay compo', 'workers compo'])
        reason = 'title_or_media_reference'
    elif word == 'fire':
        keep = any(x in t for x in ['sure fire', 'sure-fire', 'on fire', 'fire way'])
        reason = 'literal_or_proper_name_reference'
    elif word == 'pregos':
        keep = 'prego' not in t or 'pregos' in t
        if 'prego' in t and 'pregos' not in t:
            keep = False
        reason = 'literal_or_proper_name_reference'
    elif word == 'AWOL':
        keep = True
    elif word == 'mozzie':
        keep = not any(x in t for x in [' by mozzie', 'thanks mozzie', 'skeeter and pep pep', 'meet plum, skeeter'])
        reason = 'proper_name_or_team_reference'
    elif word == 'grub':
        keep = 'grub steak' not in t and 'http://' not in t
        reason = 'proper_name_or_team_reference'
    elif word == 'annihilated':
        keep = not any(x in t for x in ['http://', 'https://', 'video', 'porn', 'tube8'])
        reason = 'title_or_media_reference'
    elif word == 'God':
        keep = any(x in t for x in ['god,', 'god ', 'thank god', 'thanks god', 'oh god']) and not any(
            x in t for x in ['genesis ', 'believe in god', 'just letting god', 'god commands', 'god comes to']
        )
        reason = 'literal_or_proper_name_reference'
    elif word == 'next-level':
        keep = not any(x in t for x in ['http://', 'https://', 'mixtape', 'event', 'title'])
        reason = 'title_or_media_reference'
    elif word in {'motherfucking', 'skeevy', 'crappy', 'sicc', 'snitch', 'bumfuck', 'rachet', 'gunt', 'kosher', 'gansta', 'gangsta', 'conniption', 'DFTBA', 'poopy', 'shiesty', 'thirsty'}:
        keep = True
    elif word == 'gridlock':
        keep = 'http://' not in t and 'https://' not in t
        reason = 'title_or_media_reference'
    elif word == 'spec':
        keep = any(x in t for x in ['secret spec', 'my spec', 'his spec', 'her spec', 'spec ops pussies'])
        reason = 'literal_or_proper_name_reference'
    elif word == 'skeeter':
        keep = any(x in t for x in ['skeeter-sucked', 'skeeter sucked', 'skeeter remedy', 'call me skeeter']) and not any(
            x in t for x in [' happy wed', 'lets connect soon', 'skeeter and pep pep', 'patti mayonaise']
        )
        reason = 'proper_name_or_team_reference'
    elif word == 'walkie':
        keep = 'walkie talkie' in t or 'walkie-talkie' in t
        reason = 'literal_or_proper_name_reference'
    elif word == 'gorp':
        keep = 'trail mix' in t or 'gorp' in t and 'http://' not in t
        reason = 'title_or_media_reference'
    elif word == 'spam':
        keep = any(x in t for x in ['spam them', 'spamming', 'dont spam', "don't spam"])
        reason = 'literal_or_proper_name_reference'
    elif word == 'bowl':
        keep = False
        reason = 'literal_or_proper_name_reference'
    elif word == 'Bible-thumping':
        keep = True
    elif word == 'whooty':
        keep = True
    elif word == 'pecker':
        keep = not any(x in t for x in ['woody wood pecker', 'woodpecker'])
        reason = 'literal_or_proper_name_reference'
    elif word == 'pedo':
        keep = 'que pedo' not in t and 'what pedo' not in t
        reason = 'literal_or_proper_name_reference'
    elif word == 'lame-o':
        keep = True
    elif word == 'tool':
        keep = not any(
            x in t for x in ['freeware-tool', 'useful tool', 'campaign tool', 'tool box', 'web-based tool', 'simple tool']
        )
        reason = 'literal_or_proper_name_reference'
    elif word == 'money':
        keep = not any(x in t for x in ['money bag', 'tax money', 'spend her money', 'waste of money']) and 'gettin money' in t
        reason = 'literal_or_proper_name_reference'
    elif word == 'wang':
        keep = any(x in t for x in ['pulling my wang', 'love you bitches. and wang'])
        reason = 'proper_name_or_team_reference'
    elif word == 'gnarly':
        keep = True
    elif word == 'badass':
        keep = True
    elif word == 'zombie':
        keep = any(x in t for x in ['zombie movie', 'like a zombie', 'feel like a zombie'])
        reason = 'title_or_media_reference'
    elif word == 'sport':
        keep = any(x in t for x in ['good sport', 'spoil sport', 'sport hunt', 'sport these'])
        reason = 'literal_or_proper_name_reference'
    else:
        # Conservative fallback: keep live informal/evaluative rows without obvious link/title shells.
        keep = not any(x in t for x in ['http://', 'https://', 'new post:', 'rt @', 'video:', 'news:']) and any(
            x in t for x in [' lol', 'lmao', 'lmfao', 'haha', 'ugh', 'damn', 'wtf', '!', '?']
        )
        reason = 'title_or_media_reference'

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
