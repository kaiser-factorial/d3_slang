import csv
from pathlib import Path


SOURCE = Path("genz_slang_usage_2020_2025.csv")
TERM_LOOKUP_OUTPUT = Path("genz_term_lookup.csv")
TERM_CATEGORY_OUTPUT = Path("genz_term_categories.txt")
USAGE_CONTEXT_OUTPUT = Path("genz_usage_contexts.txt")


def main() -> None:
    term_lookup = set()
    term_categories = set()
    usage_contexts = set()

    with SOURCE.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            term_lookup.add(
                (
                    (row.get("slang_term") or "").strip(),
                    (row.get("term_category") or "").strip(),
                    (row.get("term_meaning") or "").strip(),
                )
            )
            term_categories.add((row.get("term_category") or "").strip())
            usage_contexts.add((row.get("usage_context") or "").strip())

    with TERM_LOOKUP_OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["slang_term", "term_category", "term_meaning"])
        for record in sorted(term_lookup, key=lambda item: item[0].lower()):
            writer.writerow(record)

    with TERM_CATEGORY_OUTPUT.open("w", encoding="utf-8") as outfile:
        for value in sorted(v for v in term_categories if v):
            outfile.write(f"{value}\n")

    with USAGE_CONTEXT_OUTPUT.open("w", encoding="utf-8") as outfile:
        for value in sorted(v for v in usage_contexts if v):
            outfile.write(f"{value}\n")

    print(f"Wrote {len(term_lookup)} rows to {TERM_LOOKUP_OUTPUT.name}")
    print(f"Wrote {len([v for v in term_categories if v])} values to {TERM_CATEGORY_OUTPUT.name}")
    print(f"Wrote {len([v for v in usage_contexts if v])} values to {USAGE_CONTEXT_OUTPUT.name}")


if __name__ == "__main__":
    main()
