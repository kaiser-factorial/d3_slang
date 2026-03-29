import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "AWOL": {
        "term_meaning": "\"Absent Without Leave\"; missing, gone, or unexpectedly absent",
        "term_category": "description",
        "notes": "Batch 3 approved after review; acronym expansion included in quoted form.",
    },
    "bromance": {
        "term_meaning": "a close but non-romantic friendship between men",
        "term_category": "social",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "gotsta": {
        "term_meaning": "have to; gotta; must; indicates obligation or necessity",
        "term_category": "behavior",
        "notes": "Batch 3 approved after review; closest Gen-Z taxonomy match.",
    },
    "snitch": {
        "term_meaning": "an informer; someone who tells on or betrays others",
        "term_category": "insult",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "lame-o": {
        "term_meaning": "an uncool, foolish, or pathetic person",
        "term_category": "insult",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "motherfucking": {
        "term_meaning": "a vulgar intensifier used to add force or emphasis",
        "term_category": "emphasis",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "rachet": {
        "term_meaning": "trashy, messy, low-class, or badly put together",
        "term_category": "description",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "shiesty": {
        "term_meaning": "shady, sneaky, dishonest, or untrustworthy",
        "term_category": "description",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "zooted": {
        "term_meaning": "intoxicated or high",
        "term_category": "description",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
    },
    "prettyful": {
        "term_meaning": "very pretty; especially attractive",
        "term_category": "attraction",
        "notes": "Batch 3 approved after review; matched to Gen-Z taxonomy.",
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
