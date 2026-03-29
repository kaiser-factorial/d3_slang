import csv
from pathlib import Path

UPDATES = {
    "colitas": ("\"little tails\"; in this context, marijuana buds or the potent flowering tops of the plant", "drug"),
    "fidiot": ("a fucking idiot; emphatic insult blend", "insult"),
    "meme": ("a viral joke, idea, image, or cultural reference spread online", "meme"),
    "okee-doke": ("okay; all right", "social"),
    "punanni": ("vagina; female genitalia", "sex"),
    "SCNR": ("\"Sorry, Could Not Resist\"", "reaction"),
    "sploof": ("a device used to mask the smell of marijuana smoke", "drug"),
    "trisexual": ("someone willing to try anything sexually", "identity"),
    "YooKay": ("playful slang spelling for the UK / United Kingdom", "identity"),
    "zories": ("flip-flops; thong sandals", "appearance"),
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
