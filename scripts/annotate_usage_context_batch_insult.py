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


def classify_insult(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "Baltimoron":
        if contains(lowered, "#nfl", "ravens", "colts", "peyton manning", "mets", "#wwe", "#extremerules"):
            return out("sports_discussion")
        if contains(lowered, "gamertag", "#codblackops", "what games are you bringing"):
            return out("gaming")
        if contains(lowered, "john glover", "kennedy center"):
            return out("celebrity_gossip")
        if contains(lowered, "songs on blip.fm", "baltimoron edit"):
            return out("music_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "bonehead":
        if contains(lowered, "bonehead seo", "google wave?", "bonehead of the day", "media bonehead of the day", "video]:", "cnnshowbiz"):
            return out("article_sharing")
        if contains(lowered, "bonehead short sleeve shirt", "outfitters", "paintball", "binding", "shirt for"):
            return out("advertising_spam")
        if contains(lowered, "oasis", "on bass", "naked city-bonehead", "new song i love it", "bonehead's bank holiday"):
            return out("music_discussion")
        if contains(lowered, "kill bonehead", "xboxsupport"):
            return out("gaming")
        if contains(lowered, "bonehead's experience", "cold ribs", "bbq"):
            return out("food_related")
        if contains(lowered, "whoopi:", "gibson"):
            return out("celebrity_gossip")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "bonehead move", "bonehead shit"):
            return out("criticism")
        return out("commenting")

    if word == "crock":
        if contains(lowered, "crock pot", "country crock", "slow cooker", "soup", "applesauce", "beef roast", "beer cheese"):
            return out("food_related")
        if contains(lowered, "jarden", "housewareplaza", "new slow cooker", "save $0.50"):
            return out("advertising_spam")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "what a crock", "crock of shit", "crock of poo poo"):
            return out("criticism")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "fidiot":
        if contains(lowered, "great word", "can i borrow it", "thanks for the word", "if you're going to call someone", "what fidiot would buy those"):
            return out("commenting")
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "i'm such a fidiot"):
            return out("self_description")
        return out("criticism")

    if word == "jabroni":
        if contains(lowered, "#superbowlsunday", "the superbowl", "generation x", "the rock voice"):
            return out("sports_discussion")
        if contains(lowered, "dirty txt messages", "birthday", "send me a number"):
            return out("casual_conversation")
        if contains(lowered, "lmaoooo", "lol", "rock bottom", "smackdown", "candy ass"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("criticism")

    if word == "jerkwad":
        if contains(lowered, "the master returns", "the pres"):
            return out("television_reference")
        if contains(lowered, "scott brown", "pricks i've ever met", "james cameron", "leno", "mcnealy"):
            return out("criticism")
        if contains(lowered, "robots"):
            return out("humor")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "lame-o":
        if contains(lowered, "#leno"):
            return out("celebrity_gossip")
        if contains(lowered, "myspace", "twitpic", "myloc.me"):
            return out("casual_conversation")
        if contains(lowered, "lmfao", "lol", "haha"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "not funny", "serious letdown", "that shits lame-o"):
            return out("criticism")
        return out("commenting")

    if word == "poopy":
        if contains(lowered, "diaper", "go poopy", "poopy change", "potty", "poopy party"):
            return out("self_description")
        if contains(lowered, "#fakepsa", "lookbook.nu", "white friends", "ivana trump"):
            return out("humor")
        if contains(lowered, "poopy pants", "poopy face", "poopy head", "poopy mouths"):
            return out("casual_conversation")
        if contains(lowered, "feel poopy", "isn't that poopy", "things poopy"):
            return out("self_description")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "slore":
        if contains(lowered, "miley cyrus"):
            return out("celebrity_gossip")
        if contains(lowered, "#ff", "school thang", "bb me", "where were u last nite", "u welcome slore", "don't even try 2 bring me down"):
            return out("casual_conversation")
        if contains(lowered, "lol", "lmao", "hahahah", "hurted lolsz"):
            return out("humor")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("criticism")

    if word == "snitch":
        if contains(lowered, "dealsnitcher.com", "snitch more pay less"):
            return out("advertising_spam")
        if contains(lowered, "fbi snitch", "ronald reagan", "offthetrax.com"):
            return out("article_sharing")
        if contains(lowered, "#letsbehonest", "you bet not snitch", "dry snitch", "mii sis is a snitch", "u a nigga spying"):
            return out("commenting")
        if contains(lowered, "kfc chicken", "wouldnt snitch", "gps snitch on me", "you snitch on me"):
            return out("criticism")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "tardnation":
        if contains(lowered, "@shaycarl", "vidcon", "sontard", "laurentardd", "ezratard", "#tardnation"):
            return out("casual_conversation", "Fandom/community-name use rather than insult.")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "best buy return policy"):
            return out("commenting")
        return out("casual_conversation")

    if word == "tool":
        if contains(lowered, "tool - schism", "tool the lyric"):
            return out("music_discussion")
        if contains(lowered, "sql server documentation tool", "console tool", "social media tool", "twitter marketing tool", "seo auto pilot tool", "keyword research", "tweettool", "tool used by an attacker"):
            return out("technology_discussion")
        if contains(lowered, "#affiliate", "money making machine", "follower", "get cash", "best seo", "affordable!"):
            return out("advertising_spam")
        if contains(lowered, "major tool", "garden tool?"):
            return out("criticism")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "tweeker":
        if contains(lowered, "tweeker movie"):
            return out("television_reference")
        if contains(lowered, "twitter=tweeker", "ustream"):
            return out("humor")
        if contains(lowered, "smoked/drank/passed out", "can't sleep", "feel like im livin a tweeker's lifestyle", "feel like a damn tweeker"):
            return out("self_description")
        if contains(lowered, "robbed last night", "sell magazines", "tweeker neighbors", "calling me a tweeker", "your a tweeker"):
            return out("commenting")
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("criticism")

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
    insult_path = BATCH_DIR / "insult.csv"
    technology_path = BATCH_DIR / "technology.csv"

    insult_rows = load_csv(insult_path)
    for row in insult_rows:
        context, ironic, note = classify_insult(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    insult_overrides = {
        "7600587311": "sports_discussion",
        "7761510031": "sports_discussion",
        "7846097735": "sports_discussion",
        "7852418659": "sports_discussion",
        "10392878977": "gaming",
        "10424648539": "music_discussion",
        "11368463206": "article_sharing",
        "11723005689": "celebrity_gossip",
        "12512531206": "music_discussion",
        "12904666663": "sports_discussion",
        "16197790571": "sports_discussion",
        "20924236028": "gaming",
        "21769533283": "sports_discussion",
        "24032901281": "sports_discussion",
        "726893347213312": "gaming",
        "7447199561": "article_sharing",
        "7447646885": "advertising_spam",
        "7449826734": "music_discussion",
        "7451048915": "advertising_spam",
        "7451050433": "advertising_spam",
        "7529041488": "article_sharing",
        "8142663034": "casual_conversation",
        "8142709123": "article_sharing",
        "8147360523": "article_sharing",
        "8154934255": "advertising_spam",
        "8266023485": "gaming",
        "10200035696": "advertising_spam",
        "10200328489": "gaming",
        "10203441394": "article_sharing",
        "10618524542": "food_related",
        "10619706551": "article_sharing",
        "10619995935": "music_discussion",
        "11981968766": "music_discussion",
        "18476620834": "celebrity_gossip",
        "18981775214": "advertising_spam",
        "21079277908": "music_discussion",
        "21081854739": "advertising_spam",
        "21951265905": "music_discussion",
        "23130426881": "casual_conversation",
        "26842790920": "advertising_spam",
    }
    apply_overrides(insult_rows, insult_overrides, "Insult review override: ")

    technology_rows = load_csv(technology_path)
    technology_overrides = {
        "11152995357": "casual_conversation",
        "11159280406": "advertising_spam",
        "25090910738": "technology_discussion",
        "25550222059": "technology_discussion",
        "25826109994": "casual_conversation",
        "27865381766": "technology_discussion",
        "3404798950903808": "article_sharing",
        "11734173890912256": "casual_conversation",
    }
    apply_overrides(technology_rows, technology_overrides, "Darwin audit: ")

    irony_updates = {
        "11248061288": ("false", "Frustrated complaint with LOL, but not clearly ironic."),
        "11305554244800512": ("false", "Upbeat workaround update with haha, not clear irony."),
        "19613374656552960": ("false", "Mildly amused reporting, not clearly ironic."),
        "12176904313": ("true", "Explicit `lol jk` marks tweeker use as joking."),
        "14214540216": ("true", "`hahaha jk` makes the tweeker label overtly playful."),
        "14231919470": ("true", "`Lol! Jk!` explicitly signals joking use."),
        "18337258615": ("true", "Repeated laughter plus jk makes the label teasing/nonliteral."),
        "19648396642": ("true", "`lmao jk` is explicit joking framing."),
        "27424797322": ("true", "`lmao! Jk!` makes `#tweeker` clearly ironic/teasing."),
    }
    apply_irony_updates({"technology": technology_rows, "insult": insult_rows}, irony_updates)

    write_csv(insult_path, insult_rows)
    write_csv(technology_path, technology_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (insult_rows, technology_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("insult_contexts", Counter(row["usage_context"] for row in insult_rows).most_common())
    print("insult_irony", Counter(row["is_ironic"] for row in insult_rows).most_common())
    print("technology_irony", Counter(row["is_ironic"] for row in technology_rows).most_common())


if __name__ == "__main__":
    main()
