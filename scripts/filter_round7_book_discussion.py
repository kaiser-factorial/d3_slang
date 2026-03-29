import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / '2010_tweets_slang_filtering_working.csv'

keep_ids = {
    '7545338532',
    '7561703187',
    '7875250124',
    '9215698970',
    '10103475694',
    '10553702510',
    '13625583541',
    '14186026292',
    '14351862005',
    '14352065070',
    '15722118124',
    '19107602099',
    '19699588441',
    '20740109387',
    '21086586020',
    '22209824126',
    '25268330822',
    '25912041050',
    '29068243910',
    '4354495400116224',
    '15976189952790528',
}

drop_ids = {
    '7718472722',
    '9672261878',
    '10574444390',
    '10576134852',
    '10578291993',
    '10593514064',
    '10593515113',
    '10632952625',
    '10679004993',
    '14541638617',
    '14541673984',
    '19098503380',
    '19113676057',
    '19214549661',
    '19265224931',
    '29493906747',
    '29502909056',
    '15072674090848256',
    '9837193457',
    '11852621195',
    '11853595697',
    '11875785062',
    '6018788579352576',
    '7476573302',
    '7319087632',
}

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())

for row in rows:
    if row['usage_context'] != 'book_discussion':
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
    elif word == 'bodice-ripper':
        if any(
            x in t
            for x in [
                'reading my',
                "it's a bodice ripper",
                'its a bodice ripper',
                'good bodice ripper',
                'first bodice-ripper',
                'bring on the bodice ripper',
                'bodice ripper books',
                'version of a bodice-ripper',
            ]
        ):
            keep = True
        elif any(
            x in t
            for x in [
                'http://',
                'https://',
                'npr',
                'beyond the bodice ripper',
                'our steamy bodice-ripper wedding',
            ]
        ):
            keep = False
        else:
            keep = True
    elif word in {'glitterati', 'compy'}:
        keep = True
    elif word in {'carny', 'rad', 'hells', 'booty'}:
        keep = False
    else:
        keep = False

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
