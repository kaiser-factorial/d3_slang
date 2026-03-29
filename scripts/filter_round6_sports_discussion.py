import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_words = {
    'Baltimoron',
    'BFFL',
    'F2F',
    'annihilated',
    'badass',
    'bupkis',
    'dafuq',
    'dang',
    'hells',
    'jabroni',
    'next-level',
    'okee-doke',
    'rad',
    'sesh',
    'tenner',
    'wut',
    'zounds',
}

drop_words = {
    'CBA',
    'TBA',
    'bowl',
    'carny',
    'chones',
    'compy',
    'locks',
    'money',
    'rehab',
    'revert',
    'spec',
    'threads',
    'wang',
}

headline_markers = (
    'http://',
    'https://',
    'fresh off the press',
    'new post:',
    'nbc sports',
    'rt @',
    '#contest',
)

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())
keep_ids = {'7385666209', '7428344082', '10406155201', '9001924652'}

for row in rows:
    if row['usage_context'] != 'sports_discussion':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = False
    reason = 'literal_or_topic_reference'

    if row['id'] in keep_ids:
        keep = True
    elif word in keep_words:
        keep = True
    elif word in drop_words:
        if word == 'money' and 'money may' in t:
            keep = False
            reason = 'proper_name_or_team_reference'
        else:
            keep = False
            reason = 'literal_or_proper_name_reference'
    elif word == 'a-list':
        keep = 'http://' not in t and 'https://' not in t and 'field after day one' not in t
        reason = 'literal_or_proper_name_reference'
    elif word == 'sport':
        keep = any(x in t for x in ['good sport', 'spoil sport'])
        reason = 'literal_or_proper_name_reference'
    elif word == 'streak':
        keep = not any(x in t for x in headline_markers)
        reason = 'literal_or_proper_name_reference'
    elif word == 'roshambo':
        keep = any(x in t for x in ['rock-paper-scissors', 'roshambo tourney', 'watching roshambo right now'])
        reason = 'proper_name_or_team_reference'
    elif word == 'mosey':
        keep = 'roger mosey' not in t
        reason = 'proper_name_or_team_reference'
    elif word == 'booty':
        keep = True
    else:
        keep = any(
            x in t
            for x in [
                ' lol',
                'lmao',
                'lmfao',
                'haha',
                'damn',
                'whoop',
                'badass',
                'jabroni',
                'hells yes',
                'dang',
            ]
        )
        reason = 'literal_or_topic_reference'

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
