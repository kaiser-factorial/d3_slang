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
    '8039422142',  # exclamatory God
    '8722111090',  # informal God blessing in author voice
    '7583961843',  # freckle face slang descriptor
    '7631327783',  # plastered = drunk
    '7725246172',  # figurative "throat is on fire"
}

drop_ids = {
    '8600468264',  # zombie process status
    '7634383525',  # "zombie" concept/title reference
    '7934278206',  # devotional God
    '7934279133',
    '8039420026',
    '8039421002',
    '8383900479',
    '8383901239',
    '9377268829',
    '9377276368',
    '9924329836',
    '9924329851',
    '10007901863',
    '10312652236',
    '10659596176',
    '11871326877',
    '11871329472',  # God of War
    '11871333023',
    '12137012871',
    '12186255680',
    '7529094449',  # freckle handle
    '7531686272',
    '7533625970',
    '7976473279',  # lyric/literal freckle
    '7977321040',
    '7978650239',
    '7978668677',
    '8003929004',
    '7399603316',  # literal plastered/decorating
    '7717307907',  # literal fire alarm
    '7717308682',  # fired from job
    '8188561048',  # title/metaphoric phrase, not slang token use
    '29267523721',
    '4037828308635648',
    '9574111994',  # son's blankie, not self slang use
    '12266483480',
    '7727418075',  # technical revert
    '11422715212',
    '11549267128',
    '11550459314',
    '14178924590',
    '14428626880',
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'self_description':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'literal_or_proper_name_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word in {
        'CBA', 'mosey', 'zooted', 'gotsta', 'conniption', 'chillax',
        'mozzie', 'compy', 'gag', 'sucky', 'lowkey', 'KMT',
        'motherfucking', 'tweeker', 'gnarly', 'skeevy', 'bomb',
        'relly', 'next-level', 'shtick', 'dang', 'shart', 'carny',
        'bumfuck', 'poopy', 'sicc', 'roofie', 'Bible-thumping'
    }:
        keep = True
    elif word == 'God':
        keep = has_any(t, ['oh god', 'ohh god', 'god! give me strength', 'god give me strength']) and not has_any(
            t, ['god bless', 'praise god', 'dear god', 'god of war', 'vision from god', 'in jesus', 'pastors', 'gospel']
        )
        reason = 'literal_or_religious_reference'
    elif word == 'zombie':
        keep = has_any(t, ['like a zombie', 'im a living zombie', "i'm a living zombie", 'be a zombie', 'may be zombie', 'feel like a zombie']) and not has_any(
            t, ['tasks:', ' zombie-', 'gonna download song', 'zombieland', 'shaun of the dead']
        )
        reason = 'title_or_technical_reference'
    elif word == 'plastered':
        keep = has_any(t, ['getting plastered', 'while plastered', 'so plastered', "i'm plastered", 'im plastered']) and not has_any(
            t, ['decorating', 'smile plastered']
        )
        reason = 'literal_non_slang_sense'
    elif word == 'blankie':
        keep = not has_any(t, ["sons blankie", "son's blankie", 'his blankie', 'obsessing over his blankie'])
        reason = 'literal_other_person_reference'
    elif word == 'freckle':
        keep = has_any(t, ['freckle face']) and not has_any(t, ['@freckle', 'each freckle on your face'])
        reason = 'proper_name_or_literal_reference'
    elif word == 'revert':
        keep = not has_any(
            t,
            ['snowleo', '64bit', 'opera web browser', 'chrome/firefox', 'tweetdeck', 'version 33', 'v. 34.1', 'cellphone revert back', 'new feature of my iphone']
        )
        reason = 'technical_or_metalinguistic_reference'
    elif word == 'fire':
        keep = has_any(t, ['throat is on fire', 'on fiya']) and not has_any(t, ['fire alarm', 'they fire yu', 'actually on fire'])
        reason = 'literal_non_slang_sense'
    elif word == 'thirsty':
        keep = has_any(t, ['thirsty for attention', 'thirsty for a rt', 'so thirsty for', 'stay thirsty my friends']) and not has_any(
            t, ['drink', 'water', 'juice', 'beer wagon', 'dehydration', 'dry and thirsty land']
        )
        reason = 'literal_non_slang_sense'
    elif word == 'gridlock':
        keep = has_any(t, ['my brain is in gridlock', 'mental gridlock']) and not has_any(
            t, ['traffic', 'freeeway', 'freeway', 'spring mtn', 'weather.com', 'lower manhattan']
        )
        reason = 'literal_non_slang_sense'
    elif word == 'lemme':
        keep = True
    elif word == 'money':
        keep = has_any(t, ['gettin money', 'getting money'])
        reason = 'literal_non_slang_sense'
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
