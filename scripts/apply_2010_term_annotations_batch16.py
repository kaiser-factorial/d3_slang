import csv
from pathlib import Path

UPDATES = {
    "bowl": ("a bowl; also used in compounds like \"Super Bowl\" or \"bowl game\"", "description"),
    "compo": ("short for \"composition\" or \"compensation,\" depending on context", "description"),
    "crossfade": ("a crossfade; blended transition between audio tracks or media", "technology"),
    "ent": ("short for \"entertainment\"; in some tweets also appears as dialectal \"ain't/isn't\"", "social"),
    "IBT": ("used for multiple things in this dataset, especially TOEFL iBT and organization/news acronyms", "technology"),
    "jill": ("mostly a proper name in this dataset; also appears in references like \"Jill Scott\" or \"Jack and Jill\"", "identity"),
    "wang": ("mostly a surname or proper name in this dataset; in some contexts also used as slang for penis", "identity"),
}

CSV_PATH = Path(__file__).resolve().parents[1] / "2010_terms_annotation_table.csv"

with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
    fieldnames = rows[0].keys()

for row in rows:
    if row["word"] in UPDATES:
        row["term_meaning"], row["term_category"] = UPDATES[row["word"]]

with CSV_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Applied {len(UPDATES)} term annotations to {CSV_PATH}")
