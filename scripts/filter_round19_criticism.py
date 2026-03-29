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
    '7850590993',  # tweeker as direct derogatory label
    '9748140502',  # jabroni
    '7820549102',  # crock
    '8208048951',  # fidiot
    '13103603403', # slore
    '7978964098',  # Bible-thumping
    '8361782724',  # kosher
    '7906846611',  # rapey
    '7417104996',  # pedo
    '10311960437', # bonehead
    '7542157714',  # snitch
    '7659911117',  # tool
}

drop_ids = {
    '7930735884',  # tweeker affectionate/photo-caption
    '7941870488',  # on tweeker mode
    '9264298765',  # talking about the word fidiot
    '9301354172',  # my new word is fidiot
    '7416825802',  # accusation + link shell
    '19733337491', # celebrity accusation topic shell
    '7449482313',  # Bonehead title/topic link
    '22961183008', # N bomb topic shell
    '28376238279', # N bomb topic shell
    '11401358556', # literal dietary kosher
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'criticism':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'literal_or_title_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word in {'jabroni', 'crock', 'slore', 'Bible-thumping', 'rapey', 'bonehead', 'snitch', 'tool', 'jerkwad', 'Baltimoron', 'roofie', 'gunt', 'dafuq', 'duckface', 'sploof', 'lowkey', 'shtick', 'carny', 'whadja', 'fidiot'}:
        keep = True
    elif word == 'tweeker':
        keep = not has_any(t, ['tweeker mode', 'twitter tweeker', 'twilight tweeker'])
        reason = 'non_critical_or_metalinguistic_use'
    elif word == 'kosher':
        keep = has_any(t, ["isn't kosher", 'not kosher', 'aint kosher', "ain't kosher", 'just aint kosher']) and not has_any(
            t, ['normal coke not kosher', 'kosher deli']
        )
        reason = 'literal_or_noncritical_sense'
    elif word == 'slack-jawed':
        keep = not has_any(t, ['ball being slowly lowered', 'slack-jawed amazement', 'little dieter wants to fly'])
        reason = 'noncritical_or_title_reference'
    elif word == 'pedo':
        keep = not has_any(t, ['meganlaw', 'twitanonymous', 'live on http://twitcam', 'comments in the post'])
        reason = 'topic_shell_or_link_reference'
    elif word == 'bomb':
        keep = not has_any(t, ['n bomb', 'bomb article']) and has_any(t, ['bomb shape', 'gon bomb me', 'bomb as shit'])
        reason = 'non_target_phrase_reference'
    elif word == 'annihilated':
        keep = True
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
