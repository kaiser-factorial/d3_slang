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
    '7878411922',  # tweeker joke uses slang meaning
    '8891009346',  # rachet used semantically
    '7609955186',  # shiesty used semantically
    '8173251371',  # pregos used semantically
    '7546758888',  # roofie as joke premise
    '8574977325',  # shart
    '7360775082',  # slore
    '9758566621',  # jabroni
    '15900886800', # conniption
    '7353054077',  # roshambo verb
    '7357987362',  # blumpkin metalinguistic use
    '19361579183', # dafuq
    '7761714306',  # shiznat
}

drop_ids = {
    '8667065389',  # zombie auto-post
    '8667066095',
    '8667078000',
    '8569503091',  # Cousin Skeeter reference
    '12049040267', # @Cuzo_Skeeter handle
    '7432936712',  # gag reel
    '13542783455', # gag reel
    '11290280647', # gag gifts promo
    '7422820179',  # shiesty handle
    '11408792539', # rachet handle
    '7862716886',  # roofie product/candy naming
    '9413578298',  # roofie-free slogan noise
    '10101560965', # glass of Roshambo proper-name drink
    '10104339859', # drinking Roshambo
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'humor':
        continue

    text = row['text'] or ''
    t = text.lower()
    word = row['word']
    keep = True
    reason = 'title_or_media_reference'

    if row['id'] in keep_ids:
        keep = True
    elif row['id'] in drop_ids:
        keep = False
    elif word in {'tweeker', 'lame-o', 'pregos', 'shart', 'slore', 'SCNR', 'dafuq', 'jabroni', 'conniption', 'fidiot', 'horribad', 'shiznat', 'wut', 'poopy', 'blumpkin', 'bumfuck'}:
        keep = True
    elif word == 'gag':
        keep = not has_any(t, ['gag reel', 'gag gift', 'gag gifts', 'gag factor'])
        reason = 'title_or_media_reference'
    elif word == 'roshambo':
        keep = not has_any(t, ['glass of roshambo', 'drinking roshambo'])
        reason = 'proper_name_or_title_reference'
    elif word == 'zombie':
        keep = not has_any(t, ['zombie apocalypse', 'zombie farm', 'achievement unlocked', 'auto-post', 'zombieland'])
        reason = 'title_or_game_reference'
    elif word == 'skeeter':
        keep = not has_any(t, ['cuzzin skeeter', '@cuzo_skeeter', '@skeeter', 'cousin skeeter'])
        reason = 'proper_name_or_character_reference'
    elif word == 'rachet':
        keep = '@' not in t or ' rachet ' in t or t.startswith('rachet')
        reason = 'proper_name_or_handle_reference'
    elif word == 'shiesty':
        keep = '@oo_soo_shiesty' not in t and '@shiesty' not in t
        reason = 'proper_name_or_handle_reference'
    elif word == 'roofie':
        keep = not has_any(t, ['roofie free', 'roofie-free', 'candy', 'drink name', 'bar name'])
        reason = 'product_or_slogan_reference'
    elif word == 'grub':
        keep = True
    elif word == 'linner':
        keep = True
    elif word == 'bodice-ripper':
        keep = True
    elif word == 'meme':
        keep = True
    elif word == 'rehab':
        keep = True
    elif word == 'gunt':
        keep = True
    elif word == 'pedo':
        keep = True
    elif word == 'pecker':
        keep = True
    elif word == 'fire':
        keep = True
    elif word == 'blowjob':
        keep = True
    elif word == 'punanni':
        keep = True
    elif word == 'Brotox':
        keep = True
    elif word == 'incel':
        keep = True
    elif word == 'freckle':
        keep = True
    elif word == 'whooty':
        keep = True
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
