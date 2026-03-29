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


def classify_attraction(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "McDreamy":
        if contains(lowered, "#greysanatomy", "grey's anatomy", "mcdreamy", "mcsteamy", "dr. mcdreamy", "doctor mcdreamy", "patrick dempsey", "can't buy me love"):
            return out("television_reference")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "i hope i find my mcdreamy", "meet our very own mcdreamy", "he's way hotter than mcdreamy"):
            return out("dating_context")
        return out("commenting")

    if word == "booty":
        if contains(lowered, "#nowplaying", "booty babes", "booty beats", "big booty judy", "playing:", "remix", "feat.", "jam", "song"):
            return out("music_discussion")
        if contains(lowered, "booty call", "turned me on", "squeeze", "grind from behind", "big booty", "booty pic", "ass just for you", "panties", "sex", "sexy"):
            return out("sexual_context")
        if contains(lowered, "pirates booty"):
            return out("food_related")
        if contains(lowered, "booty pop", "booty up", "avatar booty pic", "wonder booty"):
            return out("fashion_beauty")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "prettyful":
        if contains(lowered, "you look prettyful", "adorable and prettyful", "prettyful dreams", "its so awesome,prettyful and wonderful", "prettyful!!", "prettyful :)"):
            return out("compliment")
        if contains(lowered, "tattoo", "purple wig", "new bible", "t-shirt @ h&m", "notebook", "lights"):
            return out("fashion_beauty")
        if contains(lowered, "making the twitter prettyful", "layout", "twitpic", "youtube") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "rain is prettyful", "everything would be so prettyful"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("compliment")

    if word == "whooty":
        if contains(lowered, "edubb", "whooty almost at 1 million views", "youtube", "song", "jam"):
            return out("music_discussion")
        if contains(lowered, "sexy", "thong", "big booty", "spandex tights", "butt thick", "#whooty #booty"):
            return out("sexual_context")
        if contains(lowered, "official whooty", "we got whooty's now", "she's a whooty", "what's next", "burnt whooty tongue"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
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
    attraction_path = BATCH_DIR / "attraction.csv"
    appearance_path = BATCH_DIR / "appearance.csv"

    attraction_rows = load_csv(attraction_path)
    for row in attraction_rows:
        context, ironic, note = classify_attraction(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    attraction_overrides = {
        "8276688599": "article_sharing",
        "8276702898": "article_sharing",
        "8278965259": "television_reference",
        "8282998566": "television_reference",
        "8284587277": "dating_context",
        "8284872113": "television_reference",
        "8400153190": "dating_context",
        "8401350644": "television_reference",
        "8403248561": "television_reference",
        "8404572160": "celebrity_gossip",
        "8408112678": "television_reference",
        "8592307875": "celebrity_gossip",
        "8874190759": "television_reference",
        "7535862176": "sexual_context",
        "7535891420": "music_discussion",
        "7535906578": "fashion_beauty",
        "7535906971": "fashion_beauty",
        "7535908191": "fashion_beauty",
        "7535915557": "music_discussion",
        "7535918409": "music_discussion",
        "8048260438": "sexual_context",
        "8048261724": "music_discussion",
        "8048264432": "sexual_context",
        "8048278819": "fashion_beauty",
        "8783490137": "sports_discussion",
        "8783441842": "music_discussion",
        "9682402608": "music_discussion",
        "10127792194": "advertising_spam",
        "10349921746": "sexual_context",
        "10349942777": "advertising_spam",
        "11395309049": "gaming",
        "11740097529": "work_school",
        "12944803043": "advertising_spam",
        "12944804464": "food_related",
        "14083525726": "music_discussion",
        "21526624621": "commenting",
        "26321724870": "casual_conversation",
        "26321741845": "sexual_context",
        "27813034781": "gaming",
        "27847367781": "advertising_spam",
        "29456529413": "commenting",
        "25948280900": "advertising_spam",
        "6018788579352576": "book_discussion",
        "6018627035734017": "sexual_context",
        "7300026249": "commenting",
        "7304915155": "compliment",
        "7305049513": "fashion_beauty",
        "7307767639": "fashion_beauty",
        "7307974129": "casual_conversation",
        "7311081036": "religion",
        "7313134722": "fashion_beauty",
        "7313385385": "compliment",
        "7317578420": "compliment",
        "7320787942": "fashion_beauty",
        "7322433430": "compliment",
        "7575519142": "self_description",
        "7577113009": "casual_conversation",
        "7577001983": "casual_conversation",
        "7586573951": "compliment",
        "7966897282": "commenting",
        "11327996760": "casual_conversation",
        "7737118641": "fashion_beauty",
        "7737782114": "compliment",
        "7839692162": "fashion_beauty",
        "7839770331": "fashion_beauty",
        "13736915341676544": "compliment",
        "7305256440": "casual_conversation",
        "7305873070": "casual_conversation",
        "7314439808": "humor",
        "7315299564": "commenting",
        "7315340064": "commenting",
        "7315356018": "commenting",
        "8088933731": "commenting",
        "8093748488": "casual_conversation",
        "8098480553": "commenting",
        "8098537275": "commenting",
        "8103908004": "compliment",
        "8110598610": "commenting",
        "8111564619": "casual_conversation",
        "8120894978": "self_description",
        "8601495697": "commenting",
        "8612889057": "compliment",
        "8612897532": "sexual_context",
        "8612907865": "sexual_context",
        "8613061406": "casual_conversation",
        "9414638241": "dating_context",
        "9421050447": "music_discussion",
        "9439740949": "music_discussion",
        "9979005946": "casual_conversation",
        "11859984013": "sexual_context",
        "14209677360": "commenting",
        "17203529593": "commenting",
        "22572637975": "casual_conversation",
        "28378521836": "commenting",
        "9425157110104064": "music_discussion",
        "17044369135632384": "article_sharing",
    }
    apply_overrides(attraction_rows, attraction_overrides, "Manual override -> ")

    appearance_rows = load_csv(appearance_path)
    appearance_overrides = {
        "9096035068": "advertising_spam",
        "9178800515": "advertising_spam",
        "10381933642": "article_sharing",
        "10391533347": "article_sharing",
        "10395605686": "article_sharing",
        "8468551478": "fashion_beauty",
        "8468580153": "technology_discussion",
        "10744762285": "self_description",
        "22084469180": "fashion_beauty",
        "8295290847": "advertising_spam",
        "8406691407": "advertising_spam",
        "9155615133": "article_sharing",
    }
    apply_overrides(appearance_rows, appearance_overrides, "Darwin audit -> ")

    irony_updates = {
        "10127749100": ("true", "Contains 'lmaoo j/p', explicitly marking the booty shorts line as joking."),
        "7773228362": ("true", "Contains 'lol jk!', explicitly canceling the prettyful tease."),
        "17944993139": ("true", "Contains 'Jkjk lol', making the magical/prettyful line overtly playful."),
        "17982694266": ("true", "Contains 'LOLJK', explicitly marking the ugly/prettyful line as nonliteral."),
        "14127138729": ("true", "Contains 'lmao jk', making the whooty line a clear joke."),
        "14515052487": ("true", "Contains 'LMAO jk', explicitly signaling playful nonliteral use."),
        "15229726904": ("true", "Contains 'lol jk', clearly marking the #whooty line as a joke."),
    }
    apply_irony_updates(
        {
            "attraction": attraction_rows,
            "appearance": appearance_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, attraction_rows)
    sync_batch_to_master(master_rows, appearance_rows)

    write_csv(attraction_path, attraction_rows)
    write_csv(appearance_path, appearance_rows)
    write_csv(MASTER_PATH, master_rows)

    print("attraction usage_context counts:", Counter(row["usage_context"] for row in attraction_rows))
    print("attraction is_ironic counts:", Counter(row["is_ironic"] for row in attraction_rows))
    print("appearance is_ironic counts:", Counter(row["is_ironic"] for row in appearance_rows))


if __name__ == "__main__":
    main()
