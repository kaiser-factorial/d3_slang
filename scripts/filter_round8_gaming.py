import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '7728356697',
    '7964720243',
    '7529604115',
    '7713509313',
    '7720343050',
    '7741304573',
    '7775308427',
    '7878884075',
    '8081129974',
    '8070193131',
    '8190323636',
    '9901908930',
    '12740574254',
    '17424014452',
    '19634520687',
    '21768719747',
    '27351595027',
    '7799278468',
    '7799287969',
    '22732813723',
    '7977134954',
    '14392795830',
    '13059394041',
    '8505642179',
    '15971616952',
    '18389061671',
    '8642056300',
    '8266023485',
    '9256311618',
    '3795068850798592',
    '3795393431207936',
    '9903338890',
    '7588061482',
}

drop_ids = {
    '9817362243',
    '11246287734',
    '12356917179',
    '12356934206',
    '12356936380',
    '12358923747',
    '8756227802',
    '9886290464',
    '10653179519',
    '10743569520',
    '18100108327',
    '8468495298',
    '11395309049',
    '27813034781',
    '7511166733',
    '7511307245',
    '7297962584',
    '7855775340',
    '14893067244',
    '15189522332',
    '16352066030',
    '16357838179',
    '20486198275',
    '7946344710',
    '27871867689',
    '16909790466801664',
    '20870683869319168',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'gaming':
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
    elif word == 'GLHF':
        keep = 'glhf.tv' not in t
    elif word == 'spec-ops':
        keep = not any(
            x in t
            for x in [
                'youtube',
                'video guide',
                'solo guide',
                'achievement',
                'uploaded a youtube video',
                'new post:',
            ]
        )
    elif word == 'fanboy':
        keep = not any(x in t for x in ['new post', 'new blog post', 'http://kotaku.com'])
    elif word == 'money':
        keep = False
    elif word == 'streak':
        keep = 'streak master' not in t
    elif word == 'roshambo':
        keep = 'http://' not in t and 'online by playmesh' not in t
    elif word == 'carny':
        keep = 'carny ball lite' in t
    elif word == 'booty':
        keep = False
    elif word == 'zombie':
        keep = 'zombie map' not in t or 'make more zombie maps' in t
    elif word == 'bomb':
        keep = 'pipe bomb' in t
    elif word == 'hells':
        keep = 'hells yeah' in t
    elif word in {'compy', 'CBA', 'motherfucking', 'shiznat', 'zounds'}:
        keep = True
    else:
        keep = any(x in t for x in [' lol', 'lmao', 'lmfao', 'haha', 'glhf', 'fanboy', 'compy', 'hells yeah'])

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
