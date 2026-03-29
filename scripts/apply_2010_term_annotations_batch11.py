import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "shiznat": {
        "term_meaning": "something excellent, the best, or especially impressive",
        "term_category": "approval",
        "notes": "Batch 11 approved after review; matched to Gen-Z taxonomy.",
    },
    "dang": {
        "term_meaning": "mild exclamation of surprise, frustration, or emphasis",
        "term_category": "reaction",
        "notes": "Batch 11 approved after review; matched to Gen-Z taxonomy.",
    },
    "bomb": {
        "term_meaning": "excellent; very good; impressive",
        "term_category": "approval",
        "notes": "Batch 11 approved after review; fixed slang meaning used despite some literal rows.",
    },
    "plastered": {
        "term_meaning": "very drunk",
        "term_category": "behavior",
        "notes": "Batch 11 approved after review; closest taxonomy fit.",
    },
    "jabroni": {
        "term_meaning": "a foolish, obnoxious, or contemptible person",
        "term_category": "insult",
        "notes": "Batch 11 approved after review; matched to Gen-Z taxonomy.",
    },
    "jalopy": {
        "term_meaning": "an old, rundown car",
        "term_category": "description",
        "notes": "Batch 11 approved after review; closest taxonomy fit.",
    },
    "netizen": {
        "term_meaning": "an internet user; member of the online public",
        "term_category": "identity",
        "notes": "Batch 11 approved after review; matched to Gen-Z taxonomy.",
    },
    "incel": {
        "term_meaning": "\"involuntary celibate\"",
        "term_category": "identity",
        "notes": "Batch 11 approved after review; acronym-style expansion preserved in quotes.",
    },
    "pedo": {
        "term_meaning": "pedophile",
        "term_category": "sex",
        "notes": "Batch 11 approved after review; dominant term meaning used despite some noisy rows.",
    },
    "SWF": {
        "term_meaning": "\"Shockwave Flash file\"; in some contexts can also mean \"single white female\"",
        "term_category": "technology",
        "notes": "Batch 11 approved after review; dataset is overwhelmingly Flash/file-format usage.",
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
