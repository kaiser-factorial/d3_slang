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


def classify_appearance(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "Brotox":
        if contains(lowered, "song titles to rock your", "#mm"):
            return out("music_discussion")
        if contains(lowered, "doctor", "face work", "botox for men", "cosmetic", "derm", "bandwagon"):
            return out("fashion_beauty")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "lol", "that made my day", "dragons den"):
            return out("humor")
        return out("commenting")

    if word == "bling":
        if contains(lowered, "photoshop", "twitter bg", "bling text effect"):
            return out("technology_discussion")
        if contains(lowered, "tiara", "jewelry", "pendant", "bracelet", "fashion", "make-up", "styled hair", "nail polish", "bling detail", "wedding", "pots", "shoes"):
            return out("fashion_beauty")
        if contains(lowered, "spring bling", "bet", "mardi gras"):
            return out("celebrity_gossip")
        if contains(lowered, "bling blaow", "gucci", "light show", "pinky ring", "bling bling"):
            return out("music_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "chones":
        if contains(lowered, "shopping", "wearing", "pink chones", "spiderman chones", "denim chones", "dirty chones", "pants and chones"):
            return out("casual_conversation")
        if contains(lowered, "dress and chones shopping"):
            return out("fashion_beauty")
        if contains(lowered, "eat pizza in yer chones"):
            return out("food_related")
        if contains(lowered, "sexy scene", "putting his hands in my chones"):
            return out("sexual_context")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "duckface":
        if contains(lowered, "antiduckface", "year in review", "blog post", "stop making that duckface") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "pics", "picture", "photos", "album", "face", "cute duckface"):
            return out("fashion_beauty")
        if contains(lowered, "#wtf", "wtf", "aahahaha", "haha", "lol", "platypus", "p-p-p-pokerface du-du-du-duckface"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "freckle":
        if contains(lowered, "letsfreckle", "time tracking", "tickspot"):
            return out("technology_discussion")
        if contains(lowered, "beautiful", "freckles", "freckle city", "forehead", "face", "testicle", "place as him"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "bill cosby", "#quote", "freckle story"):
            return out("humor")
        return out("commenting")

    if word == "gunt":
        if contains(lowered, "gizmodo", "iphone apps", "http://post.ly/gunt"):
            return out("technology_discussion")
        if contains(lowered, "fat", "gut", "wearing spandex", "gunt girl", "what a gunt is"):
            return out("commenting")
        if contains(lowered, "ive got a proper gunt", "must shift fat", "learned the best new word", "favourite word", "explained what a gunt was"):
            return out("self_description")
        if contains(lowered, "hahah", "fantastic", "foul"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "locks":
        if contains(lowered, "gps locks", "passwords", "iphone application", "open room locks", "wheel locks", "my buggy buddy clips and locks", "blackberry", "app that locks"):
            return out("technology_discussion")
        if contains(lowered, "locks of hair", "long locks", "frizz", "hairstylist"):
            return out("fashion_beauty")
        if contains(lowered, "ballard locks"):
            return out("article_sharing")
        if contains(lowered, "open 24 hours", "locks on the doors", "change the locks", "only my locks busted"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "slack-jawed":
        if contains(lowered, "cletus", "simpsons", "sexual tyrannosaurus", "slack-jawed yokel"):
            return out("television_reference")
        if contains(lowered, "#fiestabowl", "#nflplayoffs", "the pack is back"):
            return out("sports_discussion")
        if contains(lowered, "breathtaking", "your dress"):
            return out("compliment")
        if contains(lowered, "slack jawed amazement", "i sat slack jawed", "professor told us"):
            return out("reaction")
        if contains(lowered, "hooker", "red staters", "imbeciles", "faggots", "yokels"):
            return out("criticism")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "styling":
        if contains(lowered, "joomla", "custom templates", "plugin rolled out", "sms management", "iphone", "video-based tutorial"):
            return out("technology_discussion")
        if contains(lowered, "hair styling", "makeup", "fashion", "vests are back", "styling cream", "shoot", "modeling", "styled"):
            return out("fashion_beauty")
        if contains(lowered, "free styling", "write verses", "music", "musical styling"):
            return out("music_discussion")
        if contains(lowered, "jeep liberty", "dodge ram", "gmc granite", "magnum", "aggressive styling"):
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "threads":
        if contains(lowered, "windows live movie maker", "threads workers", "text threads", "twitter about pizza", "forum", "jack threads", "meterberry code"):
            return out("technology_discussion")
        if contains(lowered, "new threads", "street gear", "clothes", "cop some new threads"):
            return out("fashion_beauty")
        if contains(lowered, "saffron threads", "chicken breasts"):
            return out("food_related")
        if contains(lowered, "techshoret", "conversation threads", "multiple threads", "community.livejournal"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "zories":
        if contains(lowered, "zories solutions", "pdms", "caesar ii", "training program"):
            return out("technology_discussion")
        if contains(lowered, "flip flops", "sandals", "tanline", "pearls, eyebrows, zories", "wearing my dad's thong", "wear 'zories' still", "new pair of zories", "shorts and zories weather"):
            return out("fashion_beauty")
        if contains(lowered, "bones"):
            return out("television_reference")
        if contains(lowered, "male fetish"):
            return out("sexual_context")
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
    appearance_path = BATCH_DIR / "appearance.csv"
    identity_path = BATCH_DIR / "identity.csv"

    appearance_rows = load_csv(appearance_path)
    for row in appearance_rows:
        context, ironic, note = classify_appearance(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    appearance_overrides = {
        "7649469175": "commenting",
        "7665163164": "humor",
        "7758778506": "humor",
        "8003514951": "celebrity_gossip",
        "8004833323": "celebrity_gossip",
        "10376938331": "article_sharing",
        "10379073953": "article_sharing",
        "10735124325": "article_sharing",
        "9155085773": "technology_discussion",
        "9155091539": "technology_discussion",
        "9155101055": "fashion_beauty",
        "9155276132": "advertising_spam",
        "9155403478": "advertising_spam",
        "9155405670": "casual_conversation",
        "9155457883": "sports_discussion",
        "9155497340": "advertising_spam",
        "9155497341": "advertising_spam",
        "9155529607": "advertising_spam",
        "9155615133": "technology_discussion",
        "9155646466": "technology_discussion",
        "9156153996": "technology_discussion",
        "9156453602": "technology_discussion",
        "10053994232": "advertising_spam",
        "10054083747": "advertising_spam",
        "10054250207": "advertising_spam",
        "10054630394": "television_reference",
        "10055191148": "advertising_spam",
        "10055338207": "music_discussion",
        "10055391056": "music_discussion",
        "10055501271": "advertising_spam",
        "10055519137": "music_discussion",
        "10445769484": "technology_discussion",
        "10445770055": "music_discussion",
        "10446069179": "advertising_spam",
        "10446187989": "advertising_spam",
        "10446291692": "article_sharing",
        "10446476006": "advertising_spam",
        "10447115070": "television_reference",
        "10447193848": "television_reference",
        "11841933354": "news_reaction",
        "11842057102": "television_reference",
        "11842125846": "advertising_spam",
        "11842399591": "music_discussion",
        "11842422638": "advertising_spam",
        "11842917738": "article_sharing",
        "14950625546": "music_discussion",
        "14950883298": "music_discussion",
        "14951107149": "music_discussion",
        "14951519357": "advertising_spam",
        "14952006926": "technology_discussion",
        "14952021384": "advertising_spam",
        "17474188471": "music_discussion",
        "18540868425": "advertising_spam",
        "18540920753": "advertising_spam",
        "18540932336": "advertising_spam",
        "18541159384": "advertising_spam",
        "18541384035": "advertising_spam",
        "18541387488": "advertising_spam",
        "18542004733": "advertising_spam",
        "29431103823": "advertising_spam",
        "29431384922": "advertising_spam",
        "29431445742": "advertising_spam",
        "29431758793": "advertising_spam",
        "29431993106": "advertising_spam",
        "29432010459": "advertising_spam",
        "29432046068": "advertising_spam",
        "29432242387": "advertising_spam",
        "7387428595": "food_related",
        "7388363019": "food_related",
        "7394485174": "food_related",
        "7396561385": "food_related",
        "9116763851": "sports_discussion",
        "9955974135": "sports_discussion",
        "9956032576": "sports_discussion",
        "7762281697": "fashion_beauty",
        "8139582966": "food_related",
        "7330559693": "article_sharing",
        "7352495538": "compliment",
        "7354190879": "fashion_beauty",
        "7379043412": "article_sharing",
        "7390909167": "article_sharing",
        "7596810009": "commenting",
        "11922707410": "criticism",
        "12180859726": "humor",
        "13344823907": "music_discussion",
        "16535455143": "casual_conversation",
        "18669803644": "commenting",
        "7621715440": "fashion_beauty",
        "7533089889": "technology_discussion",
        "7533623542": "humor",
        "7582239395": "casual_conversation",
        "7445830854": "criticism",
        "7419398060": "humor",
        "7420823198": "humor",
        "7421224022": "humor",
        "7423686312": "humor",
        "7427752806": "fashion_beauty",
        "7441029002": "criticism",
        "7444342461": "casual_conversation",
        "7398876500": "technology_discussion",
        "7398943041": "sports_discussion",
        "7398965464": "commenting",
        "7399386092": "fashion_beauty",
        "7639532974": "fashion_beauty",
        "7639832255": "fashion_beauty",
        "8142378851": "fashion_beauty",
        "7276788952": "reaction",
        "7276864987": "reaction",
        "7598736027": "reaction",
        "7623602090": "advertising_spam",
        "7623603185": "advertising_spam",
        "7623645035": "fashion_beauty",
        "7623665293": "music_discussion",
        "7623693741": "fashion_beauty",
        "7623695449": "music_discussion",
        "7623812833": "technology_discussion",
        "7623813441": "article_sharing",
        "7623855500": "article_sharing",
        "8468495298": "gaming",
        "8468551478": "commenting",
        "8469364096": "fashion_beauty",
        "8468526313": "technology_discussion",
        "7397192367": "technology_discussion",
        "7397272348": "sports_discussion",
        "7397288568": "technology_discussion",
        "7397303006": "technology_discussion",
        "7397651412": "technology_discussion",
        "7397791964": "technology_discussion",
        "7397961244": "technology_discussion",
        "8878328190": "fashion_beauty",
        "8878615460": "compliment",
        "9214021559": "technology_discussion",
        "8878403448": "food_related",
        "8295290847": "technology_discussion",
        "8406691407": "technology_discussion",
        "9617696450": "technology_discussion",
        "9785098508": "article_sharing",
        "10781532144": "fashion_beauty",
        "13171544498": "article_sharing",
        "20268478113": "sexual_context",
        "15011230091583488": "sports_discussion",
        "15012605772955648": "technology_discussion",
        "15014798517338112": "technology_discussion",
    }
    apply_overrides(appearance_rows, appearance_overrides, "Manual override -> ")

    identity_rows = load_csv(identity_path)
    identity_overrides = {
        "24705715025": "article_sharing",
        "24709298813": "article_sharing",
        "8629116216": "article_sharing",
        "9488615501": "article_sharing",
        "13891469933": "article_sharing",
        "26060862823": "article_sharing",
        "15131064024": "advertising_spam",
        "19021668099": "television_reference",
        "24308467184": "celebrity_gossip",
        "9585254633": "article_sharing",
    }
    apply_overrides(identity_rows, identity_overrides, "Darwin audit -> ")

    irony_updates = {
        "7758778506": ("true", "Thanks Brotox joke is clearly playful, not literal."),
        "9698733885": ("true", "Punchline-style fake definition marks Brotox as humorous wordplay."),
        "7419398060": ("true", "Tweet explicitly jokes about 'word for 2010 is Gunt'."),
        "7420823198": ("true", "Calls it the best new word of 2010 with playful tone."),
        "7421224022": ("true", "States 'new favourite word' playfully."),
        "7423686312": ("true", "Overtly jokey mission to spread the word 'Gunt'."),
        "20402035190923264": ("true", "Explicit 'Haha.. jk.' marks the chones line as joking."),
        "7978650239": ("true", "Contains 'hahahahaha jk lemme stop', explicitly canceling the tease."),
        "24052906505": ("true", "Contains 'lol jk', so the freckle remark is clearly playful."),
        "25477577814": ("true", "Contains '*locks door* lol jk', an explicit joking threat."),
        "27451398722": ("true", "Contains 'just kidding', making the netizen remark nonliteral."),
    }
    apply_irony_updates(
        {
            "appearance": appearance_rows,
            "identity": identity_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, appearance_rows)
    sync_batch_to_master(master_rows, identity_rows)

    write_csv(appearance_path, appearance_rows)
    write_csv(identity_path, identity_rows)
    write_csv(MASTER_PATH, master_rows)

    print("appearance usage_context counts:", Counter(row["usage_context"] for row in appearance_rows))
    print("appearance is_ironic counts:", Counter(row["is_ironic"] for row in appearance_rows))
    print("identity is_ironic counts:", Counter(row["is_ironic"] for row in identity_rows))


if __name__ == "__main__":
    main()
