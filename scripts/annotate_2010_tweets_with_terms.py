import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLEANED_TWEETS_PATH = ROOT / "2010_tweets_slang_cleaned.csv"
TERM_TABLE_PATH = ROOT / "2010_terms_annotation_table.csv"
OUTPUT_PATH = ROOT / "2010_tweets_slang_annotated.csv"


with TERM_TABLE_PATH.open(newline="") as f:
    term_rows = list(csv.DictReader(f))
    term_lookup = {
        row["word"]: {
            "term_meaning": row["term_meaning"],
            "term_category": row["term_category"],
        }
        for row in term_rows
    }

with CLEANED_TWEETS_PATH.open(newline="") as f:
    tweet_rows = list(csv.DictReader(f))
    fieldnames = list(tweet_rows[0].keys()) + ["term_meaning", "term_category"]

missing_terms = []
for row in tweet_rows:
    annotation = term_lookup.get(row["word"])
    if annotation is None:
        missing_terms.append(row["word"])
        row["term_meaning"] = ""
        row["term_category"] = ""
        continue
    row["term_meaning"] = annotation["term_meaning"]
    row["term_category"] = annotation["term_category"]

with OUTPUT_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tweet_rows)

if missing_terms:
    unique_missing = sorted(set(missing_terms))
    print(f"Missing annotations for {len(unique_missing)} terms: {', '.join(unique_missing)}")
else:
    print(f"Wrote {len(tweet_rows)} annotated rows to {OUTPUT_PATH}")
