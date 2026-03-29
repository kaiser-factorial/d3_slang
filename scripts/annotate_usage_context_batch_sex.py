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


def classify_sex(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "blowjob":
        if contains(lowered, "#porn", "#tube", "#xxx", "cum swallow", "blowjob technique", "hot blowjob", "perfect blowjob", "free sex movies", "naughty milf", "blowjob close-up") or ("http" in lowered and contains(lowered, "porn", "sex", "blowjob")):
            return out("advertising_spam")
        if contains(lowered, "seeing avatar is like getting your first blowjob", "mind a blowjob", "you can’t argue with a good blowjob", "what's the point in being president", "someday"):
            return out("commenting")
        if contains(lowered, "need a starbucks, or a blowjob", "can get a blowjob for that much", "just a blowjob", "not cheating"):
            return out("sexual_context")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("sexual_context")

    if word == "blumpkin":
        if contains(lowered, "urbandictionary", "formspring", "what a blumpkin was", "wtf is a blumkin") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "#nowplaying", "bukkake"):
            return out("music_discussion")
        if contains(lowered, "i need", "i want a blumpkin", "would u let a chick give u a #blumpkin", "gave someone a blumpkin", "gettin a blumpkin", "before i die"):
            return out("sexual_context")
        if contains(lowered, "only person in my circle", "awkward silences", "possible names for children", "should i tweet about blumpkin"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "pedo":
        if contains(lowered, "ke pedo", "q pedo", "que pedo", "estas pedo", "pedo torado"):
            return out("casual_conversation")
        if contains(lowered, "pedo bear", "pedo game", "world of warcraft", "female pedo") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "run by a 41yr old man", "makes you look like a pedo", "is a pedo", "pedo too", "grown old ass men", "trying to holla at 16", "underage girl"):
            return out("criticism")
        if contains(lowered, "don't call me pedo", "this is pedo", "pedo moment"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "pecker":
        if contains(lowered, "#sextoys", "light-up pecker", "pecker party", "stiff pecker", "sucking cock", "new item:", "party pecker") or ("http" in lowered and contains(lowered, "pecker")):
            return out("advertising_spam")
        if contains(lowered, "woody wood pecker", "wood pecker sighs", "woody wood pecker slick"):
            return out("television_reference")
        if contains(lowered, "pecker up", "piss a rock through your pecker", "change your little pecker", "twat & pecker"):
            return out("sexual_context")
        if contains(lowered, "gnats pecker", "shoot the pecker off a mosquito"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "punanni":
        if contains(lowered, "kartel", "horny rhyme wit punanni"):
            return out("music_discussion")
        if contains(lowered, "wash tjhe punanni", "punanni means rotten pussy", "best #punanni", "who's punanni do i have to eat", "angry punanni", "loves youu and thatt punanni"):
            return out("sexual_context")
        if contains(lowered, "fruit", "tropical fruit", "small child to say 'punanni'", "yelled punanni at the teacher"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "rapey":
        if contains(lowered, "last house on the left", "hostel dvd extras"):
            return out("television_reference")
        if contains(lowered, "date-rapey sounding quotes", "street boner", "ski masks look all rapey") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "rapey jokes", "who is rapey", "that sounded just a little bit rapey"):
            return out("commenting")
        if contains(lowered, "scary 'rapey'", "kind of rapey", "rapey nutcase", "celeb", "teacher", "guy", "avatar", "sounded.....rapey"):
            return out("criticism")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

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
    sex_path = BATCH_DIR / "sex.csv"
    emphasis_path = BATCH_DIR / "emphasis.csv"

    sex_rows = load_csv(sex_path)
    for row in sex_rows:
        context, ironic, note = classify_sex(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    sex_overrides = {
        "7342924408": "humor",
        "7343170927": "casual_conversation",
        "7343434710": "humor",
        "7343492104": "humor",
        "7343547715": "casual_conversation",
        "7343585423": "casual_conversation",
        "7343551396": "article_sharing",
        "7387764380": "commenting",
        "7388832439": "commenting",
        "7389072821": "commenting",
        "7389470726": "technology_discussion",
        "7443338795": "advertising_spam",
        "7444003292": "television_reference",
        "7485503233": "news_reaction",
        "7697746113": "music_discussion",
        "9173490750": "casual_conversation",
        "7352351870": "casual_conversation",
        "7358025351": "commenting",
        "7445997413": "article_sharing",
        "7713207453": "work_school",
        "7713907729": "work_school",
        "7722200282": "commenting",
        "17144884851": "casual_conversation",
        "24605029284": "humor",
        "14739157595193344": "casual_conversation",
        "7416683399": "casual_conversation",
        "7417028076": "casual_conversation",
        "7669565428": "humor",
        "7672067192": "casual_conversation",
        "7860859878": "article_sharing",
        "7861173636": "article_sharing",
        "7861447778": "article_sharing",
        "8413175053": "humor",
        "12009177417": "casual_conversation",
        "16060158809": "humor",
        "20539554086": "commenting",
        "8129823349": "humor",
        "8129946464": "humor",
        "8129965109": "humor",
        "7660663258": "advertising_spam",
        "7661166325": "commenting",
        "7661185941": "humor",
        "7661193111": "television_reference",
        "7662321820": "humor",
        "7662423187": "casual_conversation",
        "7662686962": "humor",
        "7663589535": "commenting",
        "7664389512": "advertising_spam",
        "8639827824": "advertising_spam",
        "8639829415": "advertising_spam",
        "8639963515": "casual_conversation",
        "8640220605": "television_reference",
        "7689948508": "humor",
        "8054207943": "casual_conversation",
        "8095975611": "commenting",
        "8327930223": "sexual_context",
        "8328090580": "humor",
        "8360208852": "music_discussion",
        "9205688406": "commenting",
        "9239356415": "humor",
        "9256932181": "music_discussion",
        "9274456208": "television_reference",
        "9316647653": "casual_conversation",
        "9363428137": "self_description",
        "11091029882": "television_reference",
        "7887213989": "humor",
        "7909414632": "television_reference",
        "7912294306": "storytelling",
        "8463925925": "article_sharing",
        "8471184245": "casual_conversation",
        "8639283009": "article_sharing",
        "8656363956": "music_discussion",
        "8664976343": "humor",
        "25263839886": "casual_conversation",
        "3149309059010560": "technology_discussion",
    }
    apply_overrides(sex_rows, sex_overrides, "Manual override -> ")

    emphasis_rows = load_csv(emphasis_path)
    emphasis_overrides = {
        "7326108899": "compliment",
        "7575348154": "compliment",
        "7311081036": "casual_conversation",
        "7315299564": "humor",
        "7315340064": "casual_conversation",
        "7315356018": "casual_conversation",
        "8601495697": "casual_conversation",
        "8783442059": "criticism",
        "13623853021": "music_discussion",
        "9409159594254336": "music_discussion",
    }
    apply_overrides(emphasis_rows, emphasis_overrides, "Darwin audit -> ")

    irony_updates = {}
    irony_updates = {
        "18779636468": ("true", "Explicit 'jk' marks the pedo self-label as joking."),
        "21598984727": ("true", "Contains 'PEDO! jk.', explicitly making the accusation playful."),
        "12371695079": ("true", "Contains 'Hahaha jk', so the rapey line is clearly joking."),
    }
    apply_irony_updates(
        {
            "sex": sex_rows,
            "emphasis": emphasis_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, sex_rows)
    sync_batch_to_master(master_rows, emphasis_rows)

    write_csv(sex_path, sex_rows)
    write_csv(emphasis_path, emphasis_rows)
    write_csv(MASTER_PATH, master_rows)

    print("sex usage_context counts:", Counter(row["usage_context"] for row in sex_rows))
    print("sex is_ironic counts:", Counter(row["is_ironic"] for row in sex_rows))
    print("emphasis is_ironic counts:", Counter(row["is_ironic"] for row in emphasis_rows))


if __name__ == "__main__":
    main()
