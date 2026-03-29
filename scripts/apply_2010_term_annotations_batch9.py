import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "crowdsourcing": {
        "term_meaning": "obtaining ideas, services, or content from a large distributed online group",
        "term_category": "technology",
        "notes": "Batch 9 approved after review; existing 2010-only technology category used.",
    },
    "shtick": {
        "term_meaning": "gimmick, routine, trademark style, or recurring bit",
        "term_category": "humor",
        "notes": "Batch 9 approved after review; humor chosen over behavior because the term centers on a bit/routine.",
    },
    "slack-jawed": {
        "term_meaning": "stupid-looking, vacant, or open-mouthed in a dull or stunned way",
        "term_category": "appearance",
        "notes": "Batch 9 approved after review; visual-expression meaning treated as primary.",
    },
    "GLHF": {
        "term_meaning": "\"Good Luck, Have Fun\"",
        "term_category": "social",
        "notes": "Batch 9 approved after review; acronym expansion included in quoted form.",
    },
    "whadja": {
        "term_meaning": "\"what did you\"",
        "term_category": "social",
        "notes": "Batch 9 approved after review; casual spoken contraction retained for full coverage.",
    },
    "zounds": {
        "term_meaning": "exclamation of surprise or emphasis",
        "term_category": "reaction",
        "notes": "Batch 9 approved after review; closest taxonomy fit.",
    },
    "skeeter": {
        "term_meaning": "mosquito",
        "term_category": "animals",
        "notes": "Batch 9 approved after review; existing 2010-only animals category used.",
    },
    "carny": {
        "term_meaning": "carnival worker or carnival-associated person",
        "term_category": "identity",
        "notes": "Batch 9 approved after review; matched to Gen-Z taxonomy.",
    },
    "spec": {
        "term_meaning": "specification",
        "term_category": "technology",
        "notes": "Batch 9 approved after review; low-confidence fixed meaning chosen from mixed rows.",
    },
    "freckle": {
        "term_meaning": "a small pigmented spot on the skin",
        "term_category": "appearance",
        "notes": "Batch 9 approved after review; literal but stable term added for full coverage.",
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
