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
    '7488888766',  # linner
    '7493267626',  # linner
    '7353799200',  # grub
    '7353829031',  # grub
    '7946387737',  # bomb
    '8005578348',  # bomb
}

drop_ids = {
    '7435873148',  # crock pot recipes
    '7438186278',  # crock pot
    '7820766150',  # Country Crock
    '8089544013',  # Roshambo winery
    '8151969920',  # Roshambo winery
    '9256279587',  # Spam musubi
    '9256285684',  # Spam musubi
    '12944804464', # Pirate's Booty
    '7540520173',  # literal bowl/container
    '9250758190',  # GORP headline shell
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'food_related':
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
    elif word in {'linner', 'grub'}:
        keep = True
    elif word == 'crock':
        keep = not has_any(t, ['crock pot', 'country crock', 'crock-pot'])
        reason = 'product_or_title_reference'
    elif word == 'gorp':
        keep = not has_any(t, ['gorp project', 'missoulian', 'http://', 'https://'])
        reason = 'title_or_project_reference'
    elif word == 'kosher':
        keep = True
    elif word == 'bomb':
        keep = not has_any(t, ['n bomb'])
        reason = 'non_food_phrase_reference'
    elif word == 'zooted':
        keep = True
    elif word == 'roshambo':
        keep = not has_any(t, ['winery', 'glass of roshambo', 'drinking roshambo'])
        reason = 'proper_name_or_product_reference'
    elif word == 'chones':
        keep = True
    elif word == 'bowl':
        keep = False
        reason = 'literal_non_slang_sense'
    elif word == 'spam':
        keep = not has_any(t, ['spam musubi', 'spam and eggs', 'canned spam'])
        reason = 'literal_food_product_reference'
    elif word == 'colitas':
        keep = True
    elif word == 'booty':
        keep = False
        reason = 'product_or_title_reference'
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
