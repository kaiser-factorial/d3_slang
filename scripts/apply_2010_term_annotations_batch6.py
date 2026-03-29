import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "money": {
        "term_meaning": "money; cash; wealth",
        "term_category": "money",
        "notes": "Batch 6 approved after review; matched to existing 2010-only category.",
    },
    "sport": {
        "term_meaning": "sports; athletic competition",
        "term_category": "social",
        "notes": "Batch 6 approved after review; weak taxonomy fit but retained for full coverage.",
    },
    "zombie": {
        "term_meaning": "a zombie; undead or zombie-like person/being",
        "term_category": "description",
        "notes": "Batch 6 approved after review; closest taxonomy fit.",
    },
    "revert": {
        "term_meaning": "to return to a previous state or condition",
        "term_category": "behavior",
        "notes": "Batch 6 approved after review; closest taxonomy fit.",
    },
    "walkie": {
        "term_meaning": "walkie-talkie; portable two-way radio",
        "term_category": "technology",
        "notes": "Batch 6 approved after review; matched to existing 2010-only category.",
    },
    "mozzie": {
        "term_meaning": "mosquito",
        "term_category": "animals",
        "notes": "Batch 6 approved after review; new category added because Gen-Z taxonomy did not fit.",
    },
    "threads": {
        "term_meaning": "clothes; outfit; garments",
        "term_category": "appearance",
        "notes": "Batch 6 approved after review; clothing sense used as the most stable term meaning.",
    },
    "styling": {
        "term_meaning": "fashionable grooming or dressing; being stylish",
        "term_category": "appearance",
        "notes": "Batch 6 approved after review; matched to Gen-Z taxonomy.",
    },
    "crock": {
        "term_meaning": "nonsense; rubbish; bullshit",
        "term_category": "insult",
        "notes": "Batch 6 approved after review; dismissive slang sense used over literal noun sense.",
    },
    "gridlock": {
        "term_meaning": "severe traffic congestion or complete stalemate",
        "term_category": "description",
        "notes": "Batch 6 approved after review; matched to Gen-Z taxonomy.",
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
