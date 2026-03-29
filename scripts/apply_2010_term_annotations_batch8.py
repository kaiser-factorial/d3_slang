import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "tweeker": {
        "term_meaning": "a jittery, drug-affected person, often associated with meth use",
        "term_category": "insult",
        "notes": "Batch 8 approved after review; treated as a derogatory person-label rather than a behavior term.",
    },
    "workaround": {
        "term_meaning": "a temporary fix or alternate method to get around a problem",
        "term_category": "technology",
        "notes": "Batch 8 approved after review; existing 2010-only technology category used.",
    },
    "blowjob": {
        "term_meaning": "oral sex performed on a penis",
        "term_category": "sex",
        "notes": "Batch 8 approved after review; existing 2010-only sex category used.",
    },
    "mosey": {
        "term_meaning": "move along casually or slowly",
        "term_category": "behavior",
        "notes": "Batch 8 approved after review; matched to Gen-Z taxonomy.",
    },
    "linner": {
        "term_meaning": "a meal between lunch and dinner; lunch-dinner combo",
        "term_category": "food",
        "notes": "Batch 8 approved after review; matched to Gen-Z taxonomy.",
    },
    "a-list": {
        "term_meaning": "elite, top-tier, high-status",
        "term_category": "description",
        "notes": "Batch 8 approved after review; treated as a status descriptor rather than approval.",
    },
    "pregos": {
        "term_meaning": "pregnant",
        "term_category": "description",
        "notes": "Batch 8 approved after review; closest taxonomy fit.",
    },
    "booty": {
        "term_meaning": "buttocks; sexy rear end",
        "term_category": "attraction",
        "notes": "Batch 8 approved after review; attraction chosen over appearance/sex due to sexualized desirability sense.",
    },
    "fire": {
        "term_meaning": "excellent, cool, outstanding",
        "term_category": "approval",
        "notes": "Batch 8 approved after review; fixed slang meaning used despite literal/noisy dataset rows.",
    },
    "locks": {
        "term_meaning": "hair; especially one's hairstyle or tresses",
        "term_category": "appearance",
        "notes": "Batch 8 approved after review; fixed slang meaning used despite literal/noisy dataset rows.",
    },
}


def main() -> None:
    with TABLE.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        annotation = ANNOTATIONS.get(row["word"])
        if not annotation:
            continue
        row.update(annotation)
        updated += 1

    with TABLE.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} rows in {TABLE.name}")


if __name__ == "__main__":
    main()
