import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "2010_tweets_slang_annotated.csv"
OUTPUT_PATH = ROOT / "2010_tweets_slang_usage_context_working.csv"


with SOURCE_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys()) + ["usage_context", "is_ironic", "annotation_notes"]

for row in rows:
    row["usage_context"] = ""
    row["is_ironic"] = ""
    row["annotation_notes"] = ""

rows.sort(key=lambda row: (row["term_category"], row["word"].lower(), row["date"], row["id"]))

with OUTPUT_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")
