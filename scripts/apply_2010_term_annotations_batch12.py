import csv
from pathlib import Path


TABLE = Path("2010_terms_annotation_table.csv")

ANNOTATIONS = {
    "bling": {
        "term_meaning": "flashy jewelry or flashy style/accessories",
        "term_category": "appearance",
        "notes": "Batch 12 approved after review; matched to Gen-Z taxonomy.",
    },
    "glitterati": {
        "term_meaning": "glamorous, fashionable elite; celebrity-style social set",
        "term_category": "identity",
        "notes": "Batch 12 approved after review; matched to Gen-Z taxonomy.",
    },
    "celebutante": {
        "term_meaning": "celebrity socialite; fame-based debutante type",
        "term_category": "identity",
        "notes": "Batch 12 approved after review; matched to Gen-Z taxonomy.",
    },
    "dafuq": {
        "term_meaning": "\"the fuck?\" variant expressing confusion or disbelief",
        "term_category": "reaction",
        "notes": "Batch 12 approved after review; matched to Gen-Z taxonomy.",
    },
    "blumpkin": {
        "term_meaning": "oral sex performed on someone using the toilet",
        "term_category": "sex",
        "notes": "Batch 12 approved after review; existing 2010-only sex category used.",
    },
    "Bible-thumping": {
        "term_meaning": "aggressively pious, preachy, or moralizing",
        "term_category": "religion",
        "notes": "Batch 12 approved after review; existing 2010-only religion category used.",
    },
    "blankie": {
        "term_meaning": "blanket; affectionate or childlike word for blanket",
        "term_category": "description",
        "notes": "Batch 12 approved after review; weak taxonomy fit retained for full coverage.",
    },
    "bodice-ripper": {
        "term_meaning": "melodramatic romance novel",
        "term_category": "dating",
        "notes": "Batch 12 approved after review; dataset usage clearly reflects the romance-novel genre sense.",
    },
    "bonehead": {
        "term_meaning": "stupid person; fool",
        "term_category": "insult",
        "notes": "Batch 12 approved after review; matched to Gen-Z taxonomy.",
    },
    "bupkis": {
        "term_meaning": "nothing; nothing at all",
        "term_category": "emphasis",
        "notes": "Batch 12 approved after review; emphasis used as the least-bad fit for total absence/zero.",
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
