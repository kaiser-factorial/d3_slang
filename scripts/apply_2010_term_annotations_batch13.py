import csv
from pathlib import Path

UPDATES = {
    "Baltimoron": ("a disparaging term for someone from Baltimore", "insult"),
    "Brotox": ("Botox for men; male-targeted cosmetic Botox treatment", "appearance"),
    "chones": ("underwear; underpants", "appearance"),
    "gorp": ("\"Good Ole' Raisins & Peanuts\"; trail mix or snack mix", "food"),
    "hasbian": ("someone who used to identify as a lesbian", "identity"),
    "horribad": ("extremely bad; horrifically bad", "description"),
    "preemie": ("a premature baby", "description"),
    "slore": ("a promiscuous or contemptible woman; slut-whore blend", "insult"),
    "sucky": ("bad, unpleasant, or disappointing", "description"),
    "thingamabob": ("a placeholder word for an unnamed or forgotten object", "description"),
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
