import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / "2010_tweets_slang_filtering_working.csv"
keep_words_default = ['McDreamy', 'badass', 'blankie', 'bomb', 'bro', 'bupkis', 'dafuq', 'money', 'motherfucking', 'pecker', 'rapey', 'relly', 'roofie', 'shart', 'shiznat', 'tenner', 'wut', 'zooted']
drop_name_words = ['bromance', 'carny', 'compy', 'jill', 'mozzie', 'skeeter']
keep_ids = {
    '9829383791',
    '12612597517',
    '15031601341',
    '15265763806',
    '16975820234',
    '22172141255',
    '23954291990',
    '25730823313',
    '25818912072',
    '26531524945',
    '29061650801',
    '12211782051434496',
    '18589571998552064',
}

with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fieldnames = list(rows[0].keys())
for row in rows:
    if row['usage_context'] != 'television_reference':
        continue
    text = (row['text'] or '')
    t = text.lower()
    word = row['word']
    keep = False
    if word == 'McDreamy':
        keep = True
    elif row['id'] in keep_ids:
        keep = True
    elif word == 'gnarly':
        title_or_release = any(
            x in t for x in [
                'new post:',
                'hdtv.x264-gnarly',
                'hdtv xvid-gnarly',
                'x264-gnarly',
                'xvid-gnarly',
                '#gnarly',
                'gnarly boyz',
                'gnarly enterprises',
                'gnarly football photo contest',
                'gnarly big screen tv phone',
                'rt @scifiwire: gnarly video',
                'gnarly video:',
            ]
        )
        author_voice_use = any(
            x in t for x in [
                ' pretty gnarly',
                'such a gnarly',
                'this is gnarly',
                "it's gnarly",
                ' its gnarly',
                ' was gnarly',
                ' just gnarly',
                ' these gnarly',
                'wanna see gnarly',
                ' gnarly movie',
                ' gnarly show',
                ' gnarly stunts',
                ' being gnarly',
            ]
        )
        keep = author_voice_use and not title_or_release
    elif word in drop_name_words:
        if word == 'skeeter' and any(
            x in t for x in [
                'look like skeeter',
                'looks like skeeter',
                'skeeter from doug',
                'skeeter off of doug',
                'skeeter off doug',
                'cousin skeeter looking ass',
                'look like cousin skeeter',
                'looks like cousin skeeter',
                'like cousin skeeter',
                'cousin skeeter boy',
                'looking like cousin skeeter',
            ]
        ):
            keep = True
        else:
            keep = False
    elif word in keep_words_default:
        keep = True
    else:
        if any(x in t for x in [' lol','lmao','haha','that was my show','my show','was bomb','is bomb','badass','gnarly','look like','that wass my show','was my shit','my shit','that show']) and not any(x in t for x in ['watching ','episode','season','s03e','video:']):
            keep = True
    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else 'title_or_media_reference'
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
