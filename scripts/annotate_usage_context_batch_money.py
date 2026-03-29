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


def classify_money(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "money":
        if contains(lowered, "automatic downline", "earn #money", "recurring income", "for free! its new!") or ("http" in lowered and contains(lowered, "earn", "income")):
            return out("advertising_spam")
        if contains(lowered, "download cellfire app", "blackberry or iphone only", "ipad app", "tv makes money off ads"):
            return out("technology_discussion")
        if contains(lowered, "tax money", "senior trip", "earned too much money", "lawyer", "enroll in school"):
            return out("work_school")
        if contains(lowered, "new money twinz", "pac & biggie", "mariah carey dvd", "human league"):
            return out("music_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "waste of money", "money rules u", "pile of money", "good money", "spending their tax money", "contribute money to the cause"):
            return out("commenting")
        return out("commenting")

    if word == "tenner":
        if text.startswith("@tenner") or contains(lowered, "@tenner "):
            return out("casual_conversation")
        if contains(lowered, "iphone", "spotify", "ipad app", "usb data cable", "kvms", "autocorrect"):
            return out("technology_discussion")
        if contains(lowered, "lotto", "goalscorer", "bet you could", "won a tenner", "winner", "first goalscorer", "raise you a tenner"):
            return out("sports_discussion")
        if contains(lowered, "jacket", "sale", "shoes", "pair of gorgeous shoes", "reduced to a tenner", "spending that amount of money on one"):
            return out("fashion_beauty")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "owe me a tenner", "a tenner per series", "half a tenner", "for a tenner", "just a tenner", "mildly tipsy", "bank doesn't change", "amazing boyfriend, a new moped, going back to school, a tenner"):
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
    money_path = BATCH_DIR / "money.csv"
    humor_path = BATCH_DIR / "humor.csv"

    money_rows = load_csv(money_path)
    for row in money_rows:
        context, ironic, note = classify_money(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    money_overrides = {
        "8734750947": "humor",
        "8734751640": "casual_conversation",
        "8734753747": "commenting",
        "8734753889": "commenting",
        "8734754243": "technology_discussion",
        "8734754589": "commenting",
        "8734755608": "commenting",
        "8734755653": "commenting",
        "8734757687": "technology_discussion",
        "8734757824": "work_school",
        "8740978526": "casual_conversation",
        "8740978647": "commenting",
        "8740979585": "music_discussion",
        "8740979919": "advertising_spam",
        "8740980127": "work_school",
        "8740981092": "commenting",
        "8740981113": "work_school",
        "8740982411": "commenting",
        "8740982618": "work_school",
        "8740983429": "self_description",
        "9235786532": "article_sharing",
        "9235786765": "news_reaction",
        "9235790325": "humor",
        "9235790852": "work_school",
        "9235791225": "work_school",
        "9235791345": "article_sharing",
        "9467730479": "article_sharing",
        "9467730556": "advertising_spam",
        "9467730606": "advertising_spam",
        "9467730782": "advertising_spam",
        "9467730800": "article_sharing",
        "9467731282": "advertising_spam",
        "9467731768": "advertising_spam",
        "9467732106": "article_sharing",
        "9467732783": "advertising_spam",
        "9768959875": "advertising_spam",
        "9768959930": "advertising_spam",
        "9768959970": "news_reaction",
        "9768961480": "television_reference",
        "9768966503": "food_related",
        "9886285845": "advertising_spam",
        "9886286185": "music_discussion",
        "9886288685": "advertising_spam",
        "9886288726": "article_sharing",
        "9886290464": "gaming",
        "10159066326": "technology_discussion",
        "10159067390": "television_reference",
        "10159067765": "music_discussion",
        "10159067909": "advertising_spam",
        "10159068137": "advertising_spam",
        "10606170784": "article_sharing",
        "10606171932": "article_sharing",
        "10606172071": "news_reaction",
        "10606172434": "advertising_spam",
        "10606172742": "advertising_spam",
        "10606173498": "advertising_spam",
        "10606174069": "technology_discussion",
        "10653179519": "gaming",
        "10653180198": "commenting",
        "10653181172": "technology_discussion",
        "10653181653": "advertising_spam",
        "10653181696": "advertising_spam",
        "10711216177": "advertising_spam",
        "10711216948": "advertising_spam",
        "10711217469": "advertising_spam",
        "10743566800": "commenting",
        "10743567112": "music_discussion",
        "10743567351": "advertising_spam",
        "10743567401": "advertising_spam",
        "10743567911": "article_sharing",
        "10743568834": "self_description",
        "10743569520": "gaming",
        "10750810648": "music_discussion",
        "10750813650": "advertising_spam",
        "10750814604": "article_sharing",
        "11215504964": "article_sharing",
        "11215506685": "article_sharing",
        "11215507418": "article_sharing",
        "11215508014": "advertising_spam",
        "11215508402": "article_sharing",
        "11252976122": "food_related",
        "12909950798": "advertising_spam",
        "12909950885": "advertising_spam",
        "12909951010": "advertising_spam",
        "14811442381": "advertising_spam",
        "14811444682": "advertising_spam",
        "14989466671": "advertising_spam",
        "14989473686": "advertising_spam",
        "15031435915": "advertising_spam",
        "15031441876": "advertising_spam",
        "15031447474": "advertising_spam",
        "15031450181": "article_sharing",
        "15031450553": "article_sharing",
        "15031450995": "advertising_spam",
        "15031451269": "article_sharing",
        "15031452328": "music_discussion",
        "15031453129": "article_sharing",
        "15156273722": "music_discussion",
        "15156274241": "advertising_spam",
        "15156278292": "article_sharing",
        "15332978877": "celebrity_gossip",
        "15332981640": "article_sharing",
        "15332982191": "article_sharing",
        "15332984227": "advertising_spam",
        "15332986916": "article_sharing",
        "16155796160": "article_sharing",
        "16155796184": "advertising_spam",
        "16155796230": "article_sharing",
        "16155797529": "article_sharing",
        "16155798296": "advertising_spam",
        "16155798603": "advertising_spam",
        "16155799760": "advertising_spam",
        "16155801104": "advertising_spam",
        "16321866213": "casual_conversation",
        "16321866255": "music_discussion",
        "16321867673": "music_discussion",
        "16321868025": "technology_discussion",
        "16321869829": "article_sharing",
        "16321870440": "celebrity_gossip",
        "17457723373": "music_discussion",
        "17457723902": "article_sharing",
        "17457725169": "advertising_spam",
        "17457728437": "article_sharing",
        "17457728527": "article_sharing",
        "17457728740": "advertising_spam",
        "17868456647": "advertising_spam",
        "17868457196": "technology_discussion",
        "17868458642": "casual_conversation",
        "17868464338": "advertising_spam",
        "17868465904": "advertising_spam",
        "17868469232": "advertising_spam",
        "17904985195": "advertising_spam",
        "17904985280": "work_school",
        "17904985386": "advertising_spam",
        "17904986958": "advertising_spam",
        "17904987245": "work_school",
        "17904989617": "music_discussion",
        "18100105515": "sports_discussion",
        "18100107217": "advertising_spam",
        "18100107458": "article_sharing",
        "18100107545": "sports_discussion",
        "18100107921": "article_sharing",
        "18100108327": "gaming",
        "18100109532": "article_sharing",
        "19556582113": "advertising_spam",
        "19556582835": "advertising_spam",
        "19556583281": "advertising_spam",
        "19556583394": "advertising_spam",
        "19556584816": "advertising_spam",
        "19556587259": "celebrity_gossip",
        "19556587374": "advertising_spam",
        "19658392695": "music_discussion",
        "19658392806": "sports_discussion",
        "19658394350": "advertising_spam",
        "19658395253": "article_sharing",
        "19758089233": "advertising_spam",
        "19758089714": "television_reference",
        "19758090835": "advertising_spam",
        "19758090841": "advertising_spam",
        "19758091798": "sports_discussion",
        "19758092052": "advertising_spam",
        "19758092874": "storytelling",
        "20632374781": "music_discussion",
        "20632375989": "advertising_spam",
        "20632376246": "advertising_spam",
        "20632378161": "advertising_spam",
        "20632380819": "advertising_spam",
        "20632389994": "religion",
        "7316962451": "music_discussion",
        "7317084159": "casual_conversation",
        "7317402981": "casual_conversation",
        "7327629055": "humor",
        "7328660822": "fashion_beauty",
        "7328737613": "commenting",
        "7329100105": "sports_discussion",
        "7329439674": "sports_discussion",
        "7330136924": "casual_conversation",
        "7330303391": "technology_discussion",
        "7334880511": "fashion_beauty",
        "7335444839": "sports_discussion",
        "7335499244": "music_discussion",
        "7335510089": "technology_discussion",
        "7336140010": "casual_conversation",
        "7336237124": "television_reference",
        "7336271995": "technology_discussion",
        "7336317653": "technology_discussion",
        "7336457147": "food_related",
        "7574531587": "technology_discussion",
        "7578571765": "technology_discussion",
        "7579743084": "casual_conversation",
        "7588061482": "gaming",
        "7609776047": "technology_discussion",
        "7609995876": "technology_discussion",
        "7613183532": "humor",
        "8608120990": "commenting",
        "12062716818": "casual_conversation",
        "14002923759": "commenting",
        "14871045988": "technology_discussion",
        "19578818279": "casual_conversation",
        "22573259215": "self_description",
        "5009718267346944": "television_reference",
        "19424617416368128": "casual_conversation",
    }
    apply_overrides(money_rows, money_overrides, "Manual override -> ")

    humor_rows = load_csv(humor_path)
    humor_overrides = {
        "7380583554": "food_related",
        "11538008394": "article_sharing",
        "20803254763": "article_sharing",
        "20807293413": "article_sharing",
        "16625944487788544": "casual_conversation",
        "8640220605": "fashion_beauty",
        "7671365675": "advertising_spam",
        "11939661392": "television_reference",
        "12320363968": "television_reference",
        "12010395679": "television_reference",
        "27061049943": "television_reference",
        "27073608087": "television_reference",
        "15604458037": "celebrity_gossip",
        "17533423848": "television_reference",
        "19429549870": "celebrity_gossip",
        "26047875682": "television_reference",
    }
    apply_overrides(humor_rows, humor_overrides, "Darwin audit -> ")

    irony_updates = {
        "9886290884": ("true", "Contains 'jk tho', explicitly marking the money line as joking."),
        "18432842865": ("true", "Roshambo line is overt playful banter, not literal."),
        "29545378866": ("true", "Roshambo for the mom/daughter line is clearly joking."),
    }
    apply_irony_updates(
        {
            "money": money_rows,
            "humor": humor_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, money_rows)
    sync_batch_to_master(master_rows, humor_rows)

    write_csv(money_path, money_rows)
    write_csv(humor_path, humor_rows)
    write_csv(MASTER_PATH, master_rows)

    print("money usage_context counts:", Counter(row["usage_context"] for row in money_rows))
    print("money is_ironic counts:", Counter(row["is_ironic"] for row in money_rows))
    print("humor is_ironic counts:", Counter(row["is_ironic"] for row in humor_rows))


if __name__ == "__main__":
    main()
