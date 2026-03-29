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
    '13698992306',  # slack-jawed in commenting
    '21962114468',  # chones in commenting
    '8404572160',   # McDreamy in celebrity_gossip
    '8592307875',   # McDreamy in celebrity_gossip
    '15396571723',  # duckface in fashion_beauty
    '22644432469',  # duckface in fashion_beauty
    '27564423535',  # duckface in fashion_beauty
    '8171228080',   # skeevy nickname discussion
    '8179776713',   # skeevy first installment
    '7294481999',   # mozzie in casual_conversation
    '7674530729',   # mozzie word-discussion still counts
    '20523061112',  # mozzie bites in casual_conversation
    '13326441448',  # chones in commenting
    '10058279497',  # locks in commenting
    '9807631089',   # slack-jawed in commenting
    '13588660919',  # slack-jawed in commenting
    '10531508349',  # threads in commenting
    '20281146332',  # skeeter in commenting
}

drop_ids = {
    '12857526965',  # mozzie in commenting
    '16364696899',  # mozzie in commenting
    '20598113680',  # mozzie in commenting
    '12371101981',  # a-list in celebrity_gossip
    '12371522519',  # a-list in celebrity_gossip
}

for row in rows:
    if row['id'] in keep_ids:
        row['keep_for_slang_analysis'] = 'true'
        row['exclusion_reason'] = ''
    elif row['id'] in drop_ids:
        row['keep_for_slang_analysis'] = 'false'
        row['exclusion_reason'] = 'literal_or_proper_name_reference'

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
