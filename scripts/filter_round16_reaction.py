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
    '7555947338',  # Oh My God... exclamatory
    '7282414585',  # Zounds!
    '7498246850',  # WUT?
}

drop_ids = {
    '7432936003',  # sight gag
    '7696911409',  # comic gag
    '7942733562',  # gag asia title reference
    '7934278206',  # literal blessing
    '8039421002',  # devotional God
    '8383901239',  # praise God
    '8270921453',  # non-reaction "the hells"
    '9330967870',  # track/media noise
    '10385488227',  # best dang = intensifier, not reaction
}


def has_any(text: str, patterns) -> bool:
    return any(p in text for p in patterns)


for row in rows:
    if row['usage_context'] != 'reaction':
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
    elif word in {'dafuq', 'KMT', 'zounds', 'shiznat', 'wut'}:
        keep = True
    elif word == 'dang':
        keep = not has_any(t, ['best dang', 'dang theater people'])
        reason = 'non_reaction_sense'
    elif word == 'gag':
        keep = (
            has_any(t, ['*gag*', 'made me gag', 'make me gag', 'gag me', 'gag!', ' gag ', 'more snow!  gag'])
            and not has_any(t, ['sight gag', 'old "call bison', 'lady gag', 'gag asia', 'gag comic', 'romantic yg gag', 'hadoohh.. gag'])
        )
        reason = 'literal_or_title_reference'
    elif word == 'hells':
        keep = not has_any(
            t, ['hells-city', 'hells kitchen', 'nella wan hells']
        )
        reason = 'literal_or_title_reference'
    elif word == 'God':
        keep = has_any(t, ['oh my god', 'oh god', 'thank god', 'god, give me', 'god save us', 'god knows']) and not has_any(
            t, ['god bless', 'praise god', 'dear god', 'god of war', 'vision from god', 'pastors', 'gospel', 'in jesus']
        )
        reason = 'literal_or_religious_reference'
    elif word == 'slack-jawed':
        keep = True
    elif word == 'motherfucking':
        keep = True
    elif word == 'Bible-thumping':
        keep = True
    elif word == 'conniption':
        keep = True
    elif word == 'shart':
        keep = True
    elif word == 'bomb':
        keep = True
    elif word == 'lowkey':
        keep = True
    else:
        keep = True

    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else reason

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
