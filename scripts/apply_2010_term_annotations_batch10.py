import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "chillax": {
        "term_meaning": "calm down; relax; take it easy",
        "term_category": "behavior",
        "notes": "Batch 10 approved after review; matched to Gen-Z taxonomy.",
    },
    "thirsty": {
        "term_meaning": "desperate for attention, validation, or sex",
        "term_category": "behavior",
        "notes": "Batch 10 approved after additional tweet review; 2010 dataset usage is often nonliteral and attention-seeking.",
    },
    "dudette": {
        "term_meaning": "female version of \"dude\"; casual label for a woman/girl",
        "term_category": "identity",
        "notes": "Batch 10 approved after review; matched to Gen-Z taxonomy.",
    },
    "relly": {
        "term_meaning": "\"really\"; nonstandard spelling variant",
        "term_category": "emphasis",
        "notes": "Batch 10 approved after review; retained for full coverage despite noisy rows.",
    },
    "rapey": {
        "term_meaning": "sexually creepy, assaultive, or giving predatory vibes",
        "term_category": "sex",
        "notes": "Batch 10 approved after review; existing 2010-only sex category used.",
    },
    "jerkwad": {
        "term_meaning": "contemptible fool; jerk",
        "term_category": "insult",
        "notes": "Batch 10 approved after review; matched to Gen-Z taxonomy.",
    },
    "shart": {
        "term_meaning": "accidental fart-plus-shit event; to involuntarily defecate while farting",
        "term_category": "humor",
        "notes": "Batch 10 approved after review; humor chosen because usage is comic gross-out slang.",
    },
    "gayborhood": {
        "term_meaning": "neighborhood associated with gay/LGBTQ+ culture or residents",
        "term_category": "identity",
        "notes": "Batch 10 approved after review; identity/community sense treated as primary.",
    },
    "soused": {
        "term_meaning": "drunk; intoxicated",
        "term_category": "behavior",
        "notes": "Batch 10 approved after review; closest taxonomy fit.",
    },
    "skyrocket": {
        "term_meaning": "rise very quickly",
        "term_category": "description",
        "notes": "Batch 10 approved after review; matched to Gen-Z taxonomy.",
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
