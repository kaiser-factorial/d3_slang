from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path("/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj")
BATCH_DIR = ROOT / "usage_context_batches_by_term_category"
MASTER_PATH = ROOT / "2010_tweets_slang_usage_context_working.csv"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def contains(text: str, *parts: str) -> bool:
    lowered = text.lower()
    return any(part in lowered for part in parts)


def add_note(existing: str, extra: str) -> str:
    existing = (existing or "").strip()
    if not extra:
        return existing
    if not existing:
        return extra
    if extra in existing:
        return existing
    return f"{existing} | {extra}"


def classify_roofie(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if contains(lowered, "@roofie2", "hi roofie", "roofie(ruthie)"):
        return out("casual_conversation")
    if "http" in lowered:
        return out("article_sharing")
    if contains(lowered, "don't roofie me", "gonna roofie u", "slip her a roofie", "slip me a roofie", "slipped a roofie in my drink", "gave me a roofie", "give him a roofie", "date-rape drug", "roofie peoples drinks"):
        return out("sexual_context")
    if contains(lowered, "i think i drank", "did sum1 slip me a roofie", "slipped yourself a roofie", "my drink tonight", "my face thinkin it was toner", "roofie'd and can't remember"):
        return out("self_description")
    if contains(lowered, "roofie colada", "recreate the hangover", "nachos", "tweetup", "party", "champagne", "wine", "drunk", "tequila", "club", "red cup", "best lines", "lol", "haha", "haaaa", "wtf", "fml"):
        return out("humor")
    if "@" in text:
        return out("casual_conversation")
    return out("commenting")


def apply_overrides(rows: list[dict[str, str]], overrides: dict[str, str], note_prefix: str) -> None:
    by_id = {row["id"]: row for row in rows}
    for row_id, new_context in overrides.items():
        row = by_id.get(row_id)
        if not row:
            continue
        row["usage_context"] = new_context
        row["annotation_notes"] = add_note(row.get("annotation_notes", ""), f"{note_prefix}{new_context}")


def apply_irony_updates(paths_to_rows: dict[str, list[dict[str, str]]], updates: dict[str, tuple[str, str]]) -> None:
    for rows in paths_to_rows.values():
        by_id = {row["id"]: row for row in rows}
        for row_id, (new_value, reason) in updates.items():
            row = by_id.get(row_id)
            if not row:
                continue
            row["is_ironic"] = new_value
            row["annotation_notes"] = add_note(row.get("annotation_notes", ""), f"Irony audit: {reason}")


def sync_batch_to_master(master_rows: list[dict[str, str]], batch_rows: list[dict[str, str]]) -> None:
    master_by_id = {row["id"]: row for row in master_rows}
    for batch_row in batch_rows:
        master_row = master_by_id.get(batch_row["id"])
        if not master_row:
            continue
        for field in ("usage_context", "is_ironic", "annotation_notes"):
            master_row[field] = batch_row[field]


def main() -> None:
    manipulation_path = BATCH_DIR / "manipulation.csv"
    money_path = BATCH_DIR / "money.csv"

    manipulation_rows = load_csv(manipulation_path)
    for row in manipulation_rows:
        context, ironic, note = classify_roofie(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    manipulation_overrides = {
        "7546062160": "self_description",
        "7546758888": "humor",
        "7547398515": "humor",
        "7547488804": "storytelling",
        "7547526297": "casual_conversation",
        "7548684212": "casual_conversation",
        "7548750462": "casual_conversation",
        "7550539707": "casual_conversation",
        "7551414581": "humor",
        "7552391068": "humor",
        "7857866938": "casual_conversation",
        "7858433328": "casual_conversation",
        "7858605899": "casual_conversation",
        "7859381602": "music_discussion",
        "7860204867": "casual_conversation",
        "7862716886": "humor",
        "7868560586": "casual_conversation",
        "7871000277": "casual_conversation",
        "7871319864": "casual_conversation",
        "7872591241": "self_description",
        "8135502166": "criticism",
        "8136162019": "self_description",
        "8136813644": "casual_conversation",
        "8139380257": "casual_conversation",
        "8140553589": "casual_conversation",
        "8141602684": "casual_conversation",
        "8141926043": "criticism",
        "8155386896": "casual_conversation",
        "8156782067": "casual_conversation",
        "8157609834": "casual_conversation",
        "8224649695": "humor",
        "8225917658": "commenting",
        "8226951917": "television_reference",
        "8229505313": "article_sharing",
        "8244010439": "casual_conversation",
        "8246763196": "humor",
        "8248043207": "commenting",
        "8250994192": "casual_conversation",
        "8251248873": "commenting",
        "8708565389": "television_reference",
        "10654010171": "self_description",
        "12376733028": "television_reference",
        "14125297619": "television_reference",
        "16055261010": "self_description",
        "17116528724": "humor",
        "20121370989": "criticism",
        "21779860590": "humor",
        "22623513031": "humor",
        "25006073257": "casual_conversation",
        "29322644817": "casual_conversation",
        "7307197692256256": "article_sharing",
    }
    apply_overrides(manipulation_rows, manipulation_overrides, "Manual override -> ")

    money_rows = load_csv(money_path)

    irony_updates = {
        "20122488363": ("true", "Contains 'jk <3 (maybe)', explicitly framing the roofie-colada line as a joke."),
        "29310325636": ("true", "Contains 'lol j/k (kinda) :-P', making the roofie remark playful/nonliteral."),
        "20950094593": ("true", "Roofie plus viagra line is exaggerated dark humor, not literal intent."),
        "29325451843": ("true", "Contains 'LOL' with playful 'roofie the candy' wording, clearly nonliteral."),
        "11111100229623808": ("true", "Joke-format 'that someone is me' roofie line is overtly playful."),
        "19746046484": ("true", "Bonus-tenner line is obvious comic hyperbole."),
        "14385960951": ("true", "Contains exaggerated 'pay you a tenner to house them' joke phrasing."),
    }
    apply_irony_updates(
        {
            "manipulation": manipulation_rows,
            "money": money_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, manipulation_rows)
    sync_batch_to_master(master_rows, money_rows)

    write_csv(manipulation_path, manipulation_rows)
    write_csv(money_path, money_rows)
    write_csv(MASTER_PATH, master_rows)

    print("manipulation usage_context counts:", Counter(row["usage_context"] for row in manipulation_rows))
    print("manipulation is_ironic counts:", Counter(row["is_ironic"] for row in manipulation_rows))
    print("money is_ironic counts:", Counter(row["is_ironic"] for row in money_rows))


if __name__ == "__main__":
    main()
