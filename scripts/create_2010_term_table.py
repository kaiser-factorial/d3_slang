import csv
from pathlib import Path


SOURCE = Path("2010_tweets_slang_cleaned.csv")
OUTPUT = Path("2010_terms_annotation_table.csv")
FIELDNAMES = [
    "word",
    "tweet_count",
    "first_date",
    "last_date",
    "term_meaning",
    "term_category",
    "origin_platform",
    "origin_platform_confidence",
    "notes",
]


def main() -> None:
    terms: dict[str, dict[str, str | int]] = {}

    with SOURCE.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            word = (row.get("word") or "").strip()
            date = (row.get("date") or "").strip()
            if not word:
                continue

            if word not in terms:
                terms[word] = {
                    "word": word,
                    "tweet_count": 0,
                    "first_date": date,
                    "last_date": date,
                    "term_meaning": "",
                    "term_category": "",
                    "origin_platform": "",
                    "origin_platform_confidence": "",
                    "notes": "",
                }

            entry = terms[word]
            entry["tweet_count"] = int(entry["tweet_count"]) + 1
            if date and date < str(entry["first_date"]):
                entry["first_date"] = date
            if date and date > str(entry["last_date"]):
                entry["last_date"] = date

    with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for word in sorted(terms, key=str.lower):
            writer.writerow(terms[word])

    print(f"Wrote {len(terms)} rows to {OUTPUT.name}")


if __name__ == "__main__":
    main()
