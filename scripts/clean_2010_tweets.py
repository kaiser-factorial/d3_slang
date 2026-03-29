import csv
from pathlib import Path


SOURCE = Path("2010_tweets_slang.csv")
OUTPUT = Path("2010_tweets_slang_cleaned.csv")
TARGET_FIELDS = ["word", "id", "date", "text", "author_id"]


def normalize_int_string(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        return str(int(float(value)))
    except ValueError:
        return value


def build_date(row: dict[str, str]) -> str:
    year = normalize_int_string(row.get("year", ""))
    month = normalize_int_string(row.get("month", ""))
    day = normalize_int_string(row.get("day", ""))
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"


def should_drop(row: dict[str, str]) -> bool:
    # Drop malformed rows that contain no tweet metadata.
    required = ["word", "id", "year", "month", "day", "text"]
    return not all((row.get(field) or "").strip() for field in required)


def main() -> None:
    kept_rows = []
    dropped_rows = 0

    with SOURCE.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if should_drop(row):
                dropped_rows += 1
                continue

            cleaned = {
                "word": (row.get("word") or "").strip(),
                "id": normalize_int_string(row.get("id", "")),
                "date": build_date(row),
                "text": (row.get("text") or "").strip(),
                "author_id": normalize_int_string(row.get("author_id", "")),
            }
            kept_rows.append(cleaned)

    with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=TARGET_FIELDS)
        writer.writeheader()
        writer.writerows(kept_rows)

    print(f"Wrote {len(kept_rows)} rows to {OUTPUT.name}")
    print(f"Dropped {dropped_rows} malformed rows")


if __name__ == "__main__":
    main()
