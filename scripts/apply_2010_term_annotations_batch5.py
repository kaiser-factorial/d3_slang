import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "spam": {
        "term_meaning": "unsolicited bulk or junk online messages/content",
        "term_category": "technology",
        "notes": "Batch 5 approved after review; new category used because Gen-Z taxonomy did not fit.",
    },
    "fap": {
        "term_meaning": "to masturbate",
        "term_category": "behavior",
        "notes": "Batch 5 approved after review; dataset is noisy, but core slang meaning is behavioral.",
    },
    "sicc": {
        "term_meaning": "\"sick\"; can mean ill/unwell or excellent/intense",
        "term_category": "description",
        "notes": "Batch 5 approved after review; broader meaning preserves both literal and slang-positive senses.",
    },
    "TBA": {
        "term_meaning": "\"To Be Announced\"; not yet specified",
        "term_category": "description",
        "notes": "Batch 5 approved after review; acronym expansion included in quoted form.",
    },
    "kosher": {
        "term_meaning": "acceptable, proper, or legitimate",
        "term_category": "approval",
        "notes": "Batch 5 approved after review; matched to Gen-Z taxonomy.",
    },
    "poopy": {
        "term_meaning": "childish term for poop or for something gross, bad, or silly",
        "term_category": "insult",
        "notes": "Batch 5 approved after review; meaning includes both literal and figurative uses in dataset.",
    },
    "annihilated": {
        "term_meaning": "completely destroyed, defeated, or overwhelmed",
        "term_category": "description",
        "notes": "Batch 5 approved after review; matched to Gen-Z taxonomy.",
    },
    "DFTBA": {
        "term_meaning": "\"Don't Forget To Be Awesome\"",
        "term_category": "approval",
        "notes": "Batch 5 approved after review; acronym expansion included in quoted form.",
    },
    "whooty": {
        "term_meaning": "a white girl with a booty",
        "term_category": "attraction",
        "notes": "Batch 5 approved after review; matched to Gen-Z taxonomy.",
    },
    "God": {
        "term_meaning": "the deity; including use in religious reference and as exclamation/emphasis",
        "term_category": "religion",
        "notes": "Batch 5 approved after review; new category used because Gen-Z taxonomy did not fit.",
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
