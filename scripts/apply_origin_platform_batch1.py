from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj")
TABLE_PATH = ROOT / "2010_terms_annotation_table.csv"


UPDATES = {
    "BFFL": ("instant_messaging_texting", "medium"),
    "CBA": ("instant_messaging_texting", "medium"),
    "chillax": ("offline_general_slang", "medium"),
    "DFTBA": ("youtube", "high"),
    "GLHF": ("gaming", "high"),
    "bling": ("music_hiphop", "high"),
    "Brotox": ("offline_general_slang", "low"),
    "celebutante": ("offline_general_slang", "high"),
    "bromance": ("offline_general_slang", "high"),
    "netizen": ("internet_forums", "high"),
}


def main() -> None:
    with TABLE_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        word = row["word"]
        if word in UPDATES:
            origin_platform, confidence = UPDATES[word]
            row["origin_platform"] = origin_platform
            row["origin_platform_confidence"] = confidence

    with TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("updated", len(UPDATES), "terms")


if __name__ == "__main__":
    main()
