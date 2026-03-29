import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '7533089889',
    '7638791125',
    '9727274921',
    '12433766233',
    '16441208666',
    '17531567669',
    '20545978344',
    '22841341675',
}

drop_ids = {
    '7426872874',
    '7428489628',
    '7430199434',
    '7949207775',
    '7949676633',
    '7950732211',
    '7951779389',
    '7952948630',
    '7957092373',
    '8096698447',
    '8103493526',
    '8254145451',
    '8258343065',
    '9155085773',
    '9367171083',
    '9478942765',
    '10914167235',
    '10914167492',
    '12613889786',
    '14124822392',
    '15393506895',
    '15441390962',
    '27371666855',
    '27578966785',
    '27578975590',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'technology_discussion':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = False
    reason = 'product_or_technical_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word == 'twit':
        keep = True
    elif word == 'compy':
        keep = True
    elif word == 'spam':
        keep = not any(
            x in t for x in ['new state of spam', 'spam email traffic', 'report', 'phishing report']
        )
    elif word == 'workaround':
        keep = not any(
            x in t
            for x in [
                'new post:',
                'javascript workaround brings flash',
                'exchange calendar issue',
                'api errors workaround',
            ]
        )
    elif word == 'threads':
        keep = 'jack threads' not in t
    elif word == 'spec':
        keep = not any(
            x in t
            for x in [
                'computer spec survey',
                'sparql 1.1 spec',
                'pricing and spec announced',
                'spec sheet',
            ]
        )
    elif word == 'styling':
        keep = not any(x in t for x in ['template styling', 'styling content', 'tutorial'])
    elif word == 'swf':
        keep = False
    elif word == 'ibt':
        keep = False
    elif word == 'crossfade':
        keep = not any(x in t for x in ['new post:', 'video', 'youtube', 'crossfade -'])
    elif word == 'spec-ops':
        keep = not any(x in t for x in ['guide', 'new post:', 'youtube', 'video'])
    elif word == 'bling':
        keep = True
    elif word == 'freckle':
        keep = True
    elif word == 'scnr':
        keep = True
    else:
        keep = not any(
            x in t
            for x in [
                '.swf',
                'converter',
                'bytecode',
                'specification',
                'new blog post',
                'new post:',
            ]
        )

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
