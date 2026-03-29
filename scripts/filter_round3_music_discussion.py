import csv, re
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / "2010_tweets_slang_filtering_working.csv"
semantic_words = ['badass', 'bling', 'bomb', 'booty', 'bro', 'dis', 'fire', 'gnarly', 'hells', 'lemme', 'money', 'motherfucking', 'rad', 'rehab', 'sesh', 'styling', 'thirsty', 'tool', 'whooty', 'zooted']
proper_name_words = ['DFTBA', 'a-list', 'bromance', 'brotox', 'carny', 'crossfade', 'ent', 'jill', 'roshambo', 'skeeter', 'wang']
metadata_prefixes = ('now playing', 'nowplaying', '#nowplaying', 'listening to', 'check this video out', 'video:', 'i used #shazam', 'i used shazam', 'tune in to', 'my song for', 'playing a show', 'track ', '♫', 'i liked a youtube video')
eval_patterns = ['bling bling', 'is bomb', 'was the bomb', 'da bomb', 'pretty badass', 'badass', 'pretty rad', 'so rad', 'super rad', 'gnarly', 'is fire', 'fire!!!', 'thats fire', "that's fire", 'the best song ever', 'love this song', 'i love', 'cant wait', "can't wait", 'goes hard', 'pretty damn amazing', 'is bomb man']

def is_metadata(text):
    t=text.lower().strip()
    if t.startswith(metadata_prefixes):
        return True
    if ' by ' in t and any(x in t for x in ['nowplaying','listening to','check this video out','video:','shazam','radio','track']):
        return True
    if any(x in t for x in [' feat. ', ' ft. ', ' featuring ']) and 'http' in t:
        return True
    if 'http' in t and any(x in t for x in ['now playing','radio','shazam','youtube','video','watch','listen to']):
        return True
    return False

def has_author_use(text):
    t=text.lower()
    if any(p in t for p in eval_patterns):
        return True
    if any(x in t for x in [' i ', " i'm", " im ", ' my ', ' our ', ' this is ', ' that is ', ' was ', ' were ', ' lol', ' haha', ' lmfao', ' :)', ' ;)', '!!!']):
        return True
    return False

with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fieldnames = list(rows[0].keys())
for row in rows:
    if row['usage_context'] != 'music_discussion':
        continue
    text = row['text'] or ''
    word = row['word']
    t = text.lower()
    keep = False
    if word in proper_name_words:
        keep = False
    elif word in semantic_words:
        if has_author_use(text) and not (is_metadata(text) and not any(p in t for p in eval_patterns)):
            keep = True
    else:
        if has_author_use(text) and not is_metadata(text):
            keep = True
    row['keep_for_slang_analysis'] = 'true' if keep else 'false'
    row['exclusion_reason'] = '' if keep else 'title_or_media_reference'
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
