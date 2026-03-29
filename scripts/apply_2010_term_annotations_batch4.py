import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "lemme": {
        "term_meaning": "\"let me\"; nonstandard contraction used in casual speech",
        "term_category": "social",
        "notes": "Batch 4 approved after review; weak taxonomy fit but retained for full coverage.",
    },
    "gag": {
        "term_meaning": "to retch, choke, or react with disgust or nausea",
        "term_category": "reaction",
        "notes": "Batch 4 approved after tweet review; dataset usage is primarily disgust/nausea rather than modern positive slang.",
    },
    "dis": {
        "term_meaning": "\"this\"; nonstandard spelling or pronunciation used in casual speech",
        "term_category": "social",
        "notes": "Batch 4 approved after review; weak taxonomy fit but retained for full coverage.",
    },
    "wut": {
        "term_meaning": "\"what\"; nonstandard spelling often used in informal or reactive speech",
        "term_category": "reaction",
        "notes": "Batch 4 approved after review; closest Gen-Z taxonomy match.",
    },
    "rehab": {
        "term_meaning": "rehabilitation or recovery treatment, especially for addiction",
        "term_category": "behavior",
        "notes": "Batch 4 approved after review; closest Gen-Z taxonomy match.",
    },
    "tenner": {
        "term_meaning": "a ten-dollar bill or ten-pound note",
        "term_category": "money",
        "notes": "Batch 4 approved after review; new category added because Gen-Z taxonomy did not fit.",
    },
    "twit": {
        "term_meaning": "shorthand for \"Twitter\"",
        "term_category": "technology",
        "notes": "Batch 4 approved after tweet review; dataset usage is primarily Twitter-related clipping.",
    },
    "compy": {
        "term_meaning": "computer; informal clipping",
        "term_category": "technology",
        "notes": "Batch 4 approved after review; new category added because Gen-Z taxonomy did not fit.",
    },
    "gansta": {
        "term_meaning": "gangster-like; tough, swaggering, or street-styled",
        "term_category": "identity",
        "notes": "Batch 4 approved after review; matched to Gen-Z taxonomy.",
    },
    "roofie": {
        "term_meaning": "an illicit sedative drug used to incapacitate someone",
        "term_category": "manipulation",
        "notes": "Batch 4 approved after review; closest Gen-Z taxonomy match.",
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
