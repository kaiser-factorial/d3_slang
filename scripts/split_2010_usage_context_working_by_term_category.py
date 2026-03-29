import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "2010_tweets_slang_usage_context_working.csv"
OUTPUT_DIR = ROOT / "usage_context_batches_by_term_category"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


with SOURCE_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
    fieldnames = rows[0].keys()

OUTPUT_DIR.mkdir(exist_ok=True)

groups = {}
for row in rows:
    groups.setdefault(row["term_category"], []).append(row)

for category, category_rows in groups.items():
    output_path = OUTPUT_DIR / f"{slugify(category)}.csv"
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(category_rows)
    print(f"{category}: {len(category_rows)} rows -> {output_path}")
