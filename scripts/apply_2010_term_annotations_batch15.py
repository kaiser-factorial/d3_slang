import csv
from pathlib import Path

UPDATES = {
    "dogg": ("variant of \"dog\" or \"dawg\"; used as a nickname or casual term of address", "social"),
    "hypermiler": ("a driver who tries to maximize fuel efficiency", "behavior"),
    "nuker": ("a program or tool that aggressively deletes, wipes, or destroys data", "technology"),
    "roshambo": ("rock-paper-scissors; also used for a kick to the groin", "humor"),
    "sinse": ("\"since\"; nonstandard spelling variant", "social"),
    "spec-ops": ("special operations; military-style operations or related game mode/gear", "technology"),
    "streak": ("a run of repeated outcomes or a noticeable tendency or trait", "description"),
    "tardnation": ("an offensive exclamatory or group-label formation built from \"retard\"", "insult"),
    "tool": ("a foolish, obnoxious, or contemptible person", "insult"),
    "flutterby": ("playful altered form of \"butterfly\"", "description"),
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
