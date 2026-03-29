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


def classify_identity(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "carny":
        if contains(lowered, "carny town activity", "joined carny town", "left a comment for", "added a blog post", "added a discussion", "are now friends") and "http" in lowered:
            return out("advertising_spam")
        if contains(lowered, "carny ball", "facebook app", "zynga", "farmville"):
            return out("gaming")
        if contains(lowered, "carny sideshows", "forum", "book", "citadel") and "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "my new carny job", "carny coworker", "working the midway", "carny hawker", "be a carny", "carnies"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word in {"gansta", "gangsta"}:
        if contains(lowered, "#nowplaying", "now playing", "snoop dogg", "gangsta luv", "gansta love", "gansta grills", "gansta rap", "gangsta rap", "mixtape", "track", "song", "album", "lyrics", "radio", "feat.", "ft."):
            return out("music_discussion")
        if contains(lowered, "lol jk", "jkjk", " jk.", " jk ", "lol jkjk"):
            ironic = "true"
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "jill":
        if contains(lowered, "jill scott", "#nowplaying", "now playing", "pandora", "song", "concert", "album", "love again", "cross my mind"):
            return out("music_discussion")
        if contains(lowered, "jill kelly", "porn", "facial ending", "superbporn"):
            return out("sexual_context")
        if contains(lowered, "jack & jill", "#y&r", "jill foster abbott", "jill abbott", "young and the restless"):
            return out("television_reference")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "gayborhood":
        if contains(lowered, "fireworks", "happy hour place", "going to the gayborhood", "in the gayborhood", "another fabulous day", "need to pee", "staying in", "at&t is ridiculous"):
            return out("casual_conversation")
        if contains(lowered, "shows progress", "communities of color", "investigating the gayborhood", "i stole that"):
            return out("commenting")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "fanboy":
        if contains(lowered, "apple", "microsoft", "ms fanboy", "tablet", "os x", "developer"):
            return out("technology_discussion")
        if contains(lowered, "vinyl", "life without buildings", "menswear", "talented fanboy", "#snsdoh"):
            return out("music_discussion")
        if contains(lowered, "fanboy war", "fanboy wars", "xbox", "wii", "playstation", "nintendo"):
            return out("gaming")
        if contains(lowered, "football", "baseball", "basketball", "afl", "#afl", "arsenal", "chelsea", "lakers"):
            return out("sports_discussion")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "dudette":
        if contains(lowered, "lol", "lmao", "wtf", "haha") and "@" in text:
            return out("casual_conversation")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("casual_conversation")

    if word == "glitterati":
        if contains(lowered, "joan rivers", "party", "celebrating", "boat show", "nyc glitterati", "gossip", "social set"):
            return out("celebrity_gossip")
        if contains(lowered, "platform pumps", "size big foot", "fashion", "rare finds"):
            return out("fashion_beauty")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "celebutante":
        if contains(lowered, "kim kardashian", "tinsley mortimer", "socialite", "model", "actress", "guess by marciano"):
            return out("celebrity_gossip")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "netizen":
        if contains(lowered, "internet memes", "twitter glitterati", "being a good netizen", "chinese internet", "thunderbird", "web-gmail"):
            return out("technology_discussion")
        if contains(lowered, "netizen attack", "netizen need a break", "bash them", "helpful netizen"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "wang":
        if contains(lowered, "vera wang", "alexander wang", "fashion week", "wedding dress", "collection", "gown", "princess edt", "runway", "peter som", "lacoste"):
            return out("fashion_beauty")
        if contains(lowered, "wang chung", "leehom wang", "daniel wang", "now playing"):
            return out("music_discussion")
        if contains(lowered, "chien-ming wang", "#afl", "ball skills", "nationals", "golf"):
            return out("sports_discussion")
        if contains(lowered, "penis", "wank", "sex drive", "your wang", "his wang"):
            return out("sexual_context")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "hasbian":
        if contains(lowered, "dating a", "details mag", "details.com", "converted", "ex-lesbian", "former lesbian"):
            return out("dating_context")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "trisexual":
        if contains(lowered, "try anything", "what the hell does that mean", "what is a trisexual", "virgin", "sex", "shemale videos", "latin trisexual"):
            return out("sexual_context")
        if contains(lowered, "unicorn on acid", "mirite", "lol", "lmao"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "incel":
        if contains(lowered, "vote incel party", "involuntary virginity", "virgin", "hookers", "chastity"):
            return out("commenting")
        if contains(lowered, "incel support", "forum", "support"):
            return out("article_sharing")
        if contains(lowered, "learned the word incel", "so tired of incel", "dear incel"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "yookay":
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
    identity_path = BATCH_DIR / "identity.csv"
    description_path = BATCH_DIR / "description.csv"

    identity_rows = load_csv(identity_path)
    for row in identity_rows:
        context, ironic, note = classify_identity(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    identity_overrides = {
        "8172303894": "dating_context",
        "8162333169": "advertising_spam",
        "8165425160": "advertising_spam",
        "8300331143": "article_sharing",
        "8301833119": "humor",
        "8303169748": "commenting",
        "8883354183": "article_sharing",
        "9837193457": "book_discussion",
        "9838199470": "self_description",
        "9959390406": "criticism",
        "9972717551": "self_description",
        "9976221522": "advertising_spam",
        "10640471547": "advertising_spam",
        "11852621195": "book_discussion",
        "11853595697": "book_discussion",
        "11875785062": "book_discussion",
        "13281676015": "advertising_spam",
        "14893067244": "gaming",
        "15189522332": "gaming",
        "15210986903": "music_discussion",
        "15307855372": "music_discussion",
        "16352066030": "gaming",
        "16357838179": "gaming",
        "17867535792": "music_discussion",
        "20477124633": "technology_discussion",
        "20486198275": "gaming",
        "21371658525": "sports_discussion",
        "24711840822": "television_reference",
        "7434455183": "casual_conversation",
        "7434572616": "casual_conversation",
        "7434983690": "music_discussion",
        "7552151701": "music_discussion",
        "7552153000": "music_discussion",
        "7552232086": "casual_conversation",
        "7552238381": "casual_conversation",
        "8201604788": "music_discussion",
        "8201713657": "humor",
        "8201759711": "television_reference",
        "7526433512": "casual_conversation",
        "7526509664": "casual_conversation",
        "7528617734": "casual_conversation",
        "7537997397": "article_sharing",
        "7675740305": "article_sharing",
        "7679790060": "advertising_spam",
        "7545825553": "self_description",
        "8069545948": "casual_conversation",
        "8069450567": "technology_discussion",
        "8069589430": "article_sharing",
        "8070375447": "casual_conversation",
        "8070563407": "technology_discussion",
        "8070690021": "article_sharing",
        "8070822910": "technology_discussion",
        "8190323636": "gaming",
        "8190800241": "article_sharing",
        "8191482456": "compliment",
        "9226568783": "gaming",
        "9901908930": "gaming",
        "12086503058": "technology_discussion",
        "8189780970": "fashion_beauty",
        "9901844080": "casual_conversation",
        "9901998112": "celebrity_gossip",
        "10265625841": "article_sharing",
        "10288338889": "article_sharing",
        "10431586952": "fashion_beauty",
        "12902776378": "advertising_spam",
        "14351862005": "book_discussion",
        "14352065070": "book_discussion",
        "8455701539": "casual_conversation",
        "12543735639": "casual_conversation",
        "17496938017": "casual_conversation",
        "9142307720": "celebrity_gossip",
        "9145373292": "celebrity_gossip",
        "7410018422": "article_sharing",
        "7465171524": "article_sharing",
        "7467511687": "casual_conversation",
        "7721381406": "article_sharing",
        "7742835320": "technology_discussion",
        "13089488365": "article_sharing",
        "13103030401": "article_sharing",
        "7686056661": "dating_context",
        "7692757674": "article_sharing",
        "7716562578": "article_sharing",
        "7733980824": "dating_context",
        "7750053117": "commenting",
        "7346495069": "sexual_context",
        "7453453058": "humor",
        "7356618342": "humor",
        "7471084562": "casual_conversation",
        "7925773309": "humor",
        "8135209802": "humor",
        "9823218349": "humor",
        "12151853733": "article_sharing",
        "7904727391": "casual_conversation",
        "9365807445": "commenting",
        "7901168257": "celebrity_gossip",
        "7968647363": "fashion_beauty",
        "7968702983": "humor",
        "7969090195": "sexual_context",
        "9056420455": "sports_discussion",
        "9056492994": "music_discussion",
        "9056688632": "casual_conversation",
        "9328773501": "humor",
        "28900659891": "sexual_context",
        "3965082438475776": "sexual_context",
        "3966583550517248": "sexual_context",
        "7484930190": "casual_conversation",
        "8462999021": "music_discussion",
        "13734602368": "commenting",
        "7322004695": "casual_conversation",
        "7842956081": "compliment",
    }
    apply_overrides(identity_rows, identity_overrides, "Manual override -> ")

    description_rows = load_csv(description_path)
    description_overrides = {
        "7977104887": "fashion_beauty",
        "7977159900": "fashion_beauty",
        "11224305674": "commenting",
        "12900487065": "fashion_beauty",
        "13255097046": "advertising_spam",
        "14673495592": "television_reference",
        "18926151253": "television_reference",
        "18926195468": "television_reference",
        "24396827631": "advertising_spam",
        "7759178613": "article_sharing",
    }
    apply_overrides(description_rows, description_overrides, "Darwin audit -> ")

    irony_updates = {
        "7434572616": ("true", "Explicitly joking about being 'gansta' with 'lol jk'."),
        "7552238381": ("true", "Playful c-walk/'gangsta' joke marked with LMAO/LOL."),
        "7453453058": ("true", "Self-label 'trisexual' is framed as a joke with Lol/wink."),
        "7925773309": ("true", "Incel Party tweet is overt satirical campaign humor."),
        "8135209802": ("true", "Incel Party slogan is clearly satirical."),
        "22905758681": ("true", "Explicit 'J/K ;-)' marks the fanboy jab as joking."),
        "19340017549713408": ("true", "Contains 'lol jkjk', making the gangsta line clearly nonliteral."),
        "12324853582": ("true", "Contains 'JK', explicitly framing trisexual claim as a joke."),
        "8171509366": ("true", "Contains 'lol jk', so the pregos reference is playful."),
        "18288494711": ("true", "Contains 'Lol jk', marking the pregos line as nonliteral teasing."),
        "19328647932420096": ("true", "Contains 'LOL jk', so the rachet claim is clearly playful."),
        "20874861218": ("true", "Contains repeated 'jk jk', making the shiesty line overtly joking."),
        "19788913996472320": ("true", "Contains 'LOL jk', so the kill streak claim is nonliteral."),
        "20816623335": ("true", "Contains 'lol jk', explicitly joking about thingamabob."),
    }
    apply_irony_updates(
        {
            "identity": identity_rows,
            "description": description_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, identity_rows)
    sync_batch_to_master(master_rows, description_rows)

    write_csv(identity_path, identity_rows)
    write_csv(description_path, description_rows)
    write_csv(MASTER_PATH, master_rows)

    print("identity usage_context counts:", Counter(row["usage_context"] for row in identity_rows))
    print("identity is_ironic counts:", Counter(row["is_ironic"] for row in identity_rows))
    print("description is_ironic counts:", Counter(row["is_ironic"] for row in description_rows))


if __name__ == "__main__":
    main()
