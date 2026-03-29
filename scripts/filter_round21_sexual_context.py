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
    '7947277916',      # trisexual
    '7330661217',      # fap
    '7390112043',      # blowjob
    '7535862176',      # booty call
    '12032524082',     # pecker
    '14594416467513344',  # blumpkin
    '8327930223',      # punanni
    '9461030819',      # whooty
    '15389218645',     # roofie
}

drop_ids = {
    '7892876395',  # trisexual porn/title shell
    '8622886579',  # FAP Robot
    '8622886704',
    '8622886986',
    '8622887128',
    '8622887296',
    '8622887439',
    '8622887553',
    '8622887688',
    '7443993700',  # file-title porn listing
    '7698834365',  # promo/listing shell
    '7942978856',  # directory/listing shell
    '8783586924',  # booty gallery shell
    '10349951028', # youtube/title shell
    '8612897532',  # whooty promo shell
    '9960188823',  # keyword stack
    '11856260715', # keyword stack
    '12289082390', # video promo shell
    '9145776395',  # woofie pun
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'sexual_context':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'product_or_title_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word == 'trisexual':
        keep = not has_any(t, ['http://', 'https://', 'video', 'gallery', 'tube'])
        reason = 'product_or_title_reference'
    elif word == 'fap':
        keep = not has_any(t, ['fap robot', 'income streams', 'xtube']) and ('fap' in t)
        reason = 'product_or_title_reference'
    elif word == 'blowjob':
        keep = not has_any(t, ['[pre]', '[xxx]', '.wmv', 'gay, asian twink', 'gives great blowjob'])
        reason = 'product_or_title_reference'
    elif word == 'booty':
        keep = not has_any(t, ['paparazzi', 'youtube video', 'http://', 'bit.ly/']) or 'booty call' in t
        reason = 'product_or_title_reference'
    elif word == 'pecker':
        keep = True
    elif word == 'gag':
        keep = True
    elif word == 'roofie':
        keep = not has_any(t, ['woofie', 'nobody wanna rape you'])
        reason = 'non_target_joke_or_shell'
    elif word == 'whooty':
        keep = not has_any(t, ['http://', 'bit.ly/', '#video', '#nsfw', 'candid booty', 'spandex tights butt thick'])
        reason = 'product_or_title_reference'
    elif word == 'blumpkin':
        keep = True
    elif word == 'wang':
        keep = not has_any(t, ['mirrorfootball', 'pep', 'mrpeterandre'])
        reason = 'proper_name_or_nonsexual_reference'
    elif word == 'punanni':
        keep = True
    elif word in {'jill', 'lemme', 'chones', 'zories'}:
        keep = True
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
