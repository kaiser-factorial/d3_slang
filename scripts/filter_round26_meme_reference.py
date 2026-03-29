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
    '9295387895',
    '9297154128',
    '9299689143',
    '9299722882',
    '8793928487',
    '8794068570',
    '9769142688',
    '10958324693',
    '10958767013',
    '12881401914',
    '12881463201',
    '14004080548',
    '14004397136',
    '14004677623',
    '18666411120',
    '18666552394',
    '20012217196',
    '20874025574',
    '20874042694',
    '27331751350',
    '15132793805733888',
}

drop_ids = {
    '8546115151',
    '8794395448',
    '10958612278',
    '12573496126',
    '12573573287',
    '12881836694',
    '12881838954',
    '12881839750',
    '16126217147',
    '18337752040',
    '19368208485',
    '19368549247',
    '20317707840',
    '20317716207',
    '20318020488',
    '27331169450',
    '18483961473',
    '18483965303',
    '18483965909',
    '18483968720',
}

for row in rows:
    if row['usage_context'] != 'meme_reference':
        continue

    if row['id'] in keep_ids:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''
    elif row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'title_or_link_shell'
    else:
        # Keep the remaining rows by default; this bucket is small and these are
        # mostly active meme-discussion uses rather than inherited headline shells.
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
