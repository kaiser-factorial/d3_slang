import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "crappy": {
        "term_meaning": "bad, low-quality, unpleasant, or physically lousy",
        "term_category": "description",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "peeps": {
        "term_meaning": "people, especially one's friends or social group",
        "term_category": "social",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "sesh": {
        "term_meaning": "a session; a shared hangout or activity period",
        "term_category": "social",
        "notes": "Batch 2 approved after review; closest Gen-Z taxonomy match.",
    },
    "BFFL": {
        "term_meaning": "\"Best Friend For Life\"; a very close lifelong friend",
        "term_category": "social",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "bro": {
        "term_meaning": "brother or male friend; casual friendly term of address",
        "term_category": "social",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "sis": {
        "term_meaning": "sister or female friend; casual friendly term of address",
        "term_category": "social",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "lowkey": {
        "term_meaning": "understated, restrained, discreet; somewhat or to a limited degree",
        "term_category": "emphasis",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "rad": {
        "term_meaning": "cool, excellent, or impressive",
        "term_category": "approval",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
    },
    "badass": {
        "term_meaning": "tough, formidable, striking, or impressively cool",
        "term_category": "description",
        "notes": "Batch 2 approved after review; resolved to description rather than approval.",
    },
    "hells": {
        "term_meaning": "emphatic intensifier in expressions like 'hells yeah' or 'hells yes'",
        "term_category": "emphasis",
        "notes": "Batch 2 approved after review; matched to Gen-Z taxonomy.",
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
