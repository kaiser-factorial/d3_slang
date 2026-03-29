import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "skeevy": {
        "term_meaning": "disgusting, sleazy, creepy, or repulsive",
        "term_category": "description",
        "notes": "Batch 1 consensus across 3 agent reviews; matched to Gen-Z taxonomy.",
    },
    "grub": {
        "term_meaning": "food; something to eat",
        "term_category": "food",
        "notes": "Batch 1 consensus across 3 agent reviews; matched to Gen-Z taxonomy.",
    },
    "KMT": {
        "term_meaning": "kissing my teeth; an expression of annoyance, disapproval, or frustration",
        "term_category": "reaction",
        "notes": "Batch 1 consensus across 3 agent reviews; matched to Gen-Z taxonomy.",
    },
    "CBA": {
        "term_meaning": "can't be arsed; can't be bothered or unwilling to deal with something",
        "term_category": "behavior",
        "notes": "Batch 1 agent split between behavior and emotion; resolved to behavior as the closest Gen-Z fit.",
    },
    "gnarly": {
        "term_meaning": "intense, extreme, wild, or striking; sometimes bad or gross, sometimes impressive or cool",
        "term_category": "description",
        "notes": "Batch 1 reviewed against dataset evidence; 2010 usage includes both negative and positive senses, with a broader descriptive meaning.",
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
