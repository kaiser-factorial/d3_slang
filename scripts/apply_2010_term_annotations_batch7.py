import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "gangsta": {
        "term_meaning": "gangster-like; tough, swaggering, or street-styled",
        "term_category": "identity",
        "notes": "Batch 7 approved after review; aligned exactly with existing gansta entry.",
    },
    "next-level": {
        "term_meaning": "beyond ordinary; advanced, extreme, or exceptionally good",
        "term_category": "approval",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "F2F": {
        "term_meaning": "\"face to face\"; in person",
        "term_category": "social",
        "notes": "Batch 7 approved after review; acronym expansion included in quoted form.",
    },
    "duckface": {
        "term_meaning": "pouty-lipped facial pose/expression, especially for photos",
        "term_category": "appearance",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "conniption": {
        "term_meaning": "fit of anger, agitation, or hysteria",
        "term_category": "emotion",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "gunt": {
        "term_meaning": "overhanging gut/crotch area; body-shape term",
        "term_category": "appearance",
        "notes": "Batch 7 approved after review; body-feature meaning treated as primary over insultive force.",
    },
    "bumfuck": {
        "term_meaning": "an extremely remote, middle-of-nowhere place",
        "term_category": "description",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "McDreamy": {
        "term_meaning": "dream guy; ideal attractive man",
        "term_category": "attraction",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "fanboy": {
        "term_meaning": "overly enthusiastic or obsessive male fan",
        "term_category": "identity",
        "notes": "Batch 7 approved after review; matched to Gen-Z taxonomy.",
    },
    "pecker": {
        "term_meaning": "penis",
        "term_category": "sex",
        "notes": "Batch 7 approved after review; new category added because existing taxonomy did not fit cleanly.",
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
