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


def classify_reaction(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"
    note = ""

    def out(ctx: str, local_note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, local_note

    if word == "KMT":
        if "http" in lowered and contains(lowered, "kmt'ers", "taiwan foundation", "democracy"):
            return out("news_reaction", "Political/news use of KMT as party reference, not 'kissing my teeth'.")
        if contains(lowered, "#arsenal", "football", "grammys", "programme", "cbb", "summer needs to hurry"):
            return out("reaction")
        if contains(lowered, "i am crazy late", "best have a goatee", "wanted mummy", "myself"):
            return out("self_description")
        if "@" in text or contains(lowered, "lol", "haha", "playinn", "u beta", "where were u", "missed out"):
            return out("casual_conversation")
        return out("reaction")

    if word == "SCNR":
        if contains(lowered, "laser bar code scnr", "scanner", "scnr w/ bt", "trac", "software development tracker", "linux", "windows", "ipad", "oracle", "desktop virtualization"):
            return out("technology_discussion", "SCNR appears in scanner/software/tech context.")
        if "http" in lowered and contains(lowered, "blog post", "gizmodo", "bit.ly", "trim.su", "ad.vu"):
            return out("article_sharing")
        if contains(lowered, "goodnight", "have a good week", "no problem", "did it stop to suck", "@"):
            return out("casual_conversation")
        if contains(lowered, "lmfao", "hehe", "absurd", "scnr already", "handsome man", "friendship!", "who the fuck"):
            return out("humor")
        return out("humor", "SCNR usually marks a joking or teasing aside.")

    if word == "dafuq":
        if "http" in lowered and contains(lowered, "wrinkle skincare", "bit.ly", "follow", "tweetphoto", "worldstarhiphop"):
            return out("advertising_spam" if contains(lowered, "wrinkle skincare", "follow @") else "article_sharing")
        if contains(lowered, "#vols", "drew brees", "football coach"):
            return out("sports_discussion")
        if contains(lowered, "this bitch just came", "remembered a dream", "couldn't wait until you got home"):
            return out("storytelling")
        if contains(lowered, "stopped talkin to me", "he miss me", "u tryna smoke", "u asked me to smoke"):
            return out("commenting")
        if contains(lowered, "where u been", "wasssssuppp", "thankz", "you been at", "@by3_dafuq_by", "its a site where u chat"):
            return out("casual_conversation")
        if contains(lowered, "poot ass low budget movie", "on bet?"):
            return out("television_reference")
        if contains(lowered, "at work"):
            return out("work_school")
        if contains(lowered, "lol", "lmao", "haha", "lmfao"):
            return out("humor")
        return out("reaction")

    if word == "dang":
        if "http" in lowered and contains(lowered, "journey to the west", "formspring", "accountability", "boycott", "tweetphoto"):
            return out("advertising_spam" if contains(lowered, "follow me on my journey") else "article_sharing")
        if contains(lowered, "dang! dang! eyeshield 21 themesong", "#np"):
            return out("music_discussion")
        if contains(lowered, "halo burger", "olive garden", "eating fried pickles", "food sounds like a better idea"):
            return out("food_related")
        if contains(lowered, "sounders vs monterrey", "gave the game away", "#bears on the clock"):
            return out("sports_discussion")
        if contains(lowered, "oil change", "watchin the news", "ticket on campus"):
            return out("news_reaction" if "news" in lowered else "self_description")
        if contains(lowered, "my honey is off work", "caking time"):
            return out("dating_context")
        if contains(lowered, "amazing new songs", "great music"):
            return out("compliment")
        if contains(lowered, "black nail polish", "let me n dat dang"):
            return out("music_discussion")
        if contains(lowered, "@") or contains(lowered, "dang by who", "you finally unblocked me", "i was just bein nice", "time flies"):
            return out("casual_conversation")
        if contains(lowered, "lol", "lmao", "hahaha"):
            return out("humor")
        return out("reaction")

    if word == "gag":
        if "http" in lowered and contains(lowered, "open mouth gag", "leather o-ring gag", "cheap mr-s-leather", "bit.ly", "url4.eu"):
            return out("advertising_spam", "Sex-product promo/listing.")
        if "http" in lowered and contains(lowered, "youtube", "9gag", "twitpic", "formspring", "amazon xbox deal"):
            return out("article_sharing")
        if contains(lowered, "no gag reflex", "swallow", "banana", "meat", "twitterafterdark", "sucking on my dick"):
            return out("sexual_context")
        if contains(lowered, "gag gift", "9gag", "gag reel", "gag factor"):
            return out("humor")
        if contains(lowered, "made me gag", "bout to gag", "gag reflex", "smell made me gag", "making me gag"):
            return out("self_description")
        if contains(lowered, "theme song", "bitch you'll gag", "#nowplaying"):
            return out("music_discussion")
        if contains(lowered, "@") and not contains(lowered, "made me gag", "gag reflex"):
            return out("casual_conversation")
        return out("reaction")

    if word == "wut":
        if "http" in lowered and contains(lowered, "#twitter has more uptime", "youtube", "myloc.me"):
            return out("article_sharing")
        if contains(lowered, "american idol", "bad girls club"):
            return out("television_reference")
        if contains(lowered, "what workout", "opengym", "lifting"):
            return out("sports_discussion")
        if contains(lowered, "headin 2 s'pore", "seminar", "bad day", "boss sits bside me"):
            return out("work_school")
        if contains(lowered, "wut the heck", "wut?", "what the hell") and "@" not in text:
            return out("reaction")
        if contains(lowered, "@") or contains(lowered, "wut u doin", "wut yall do", "wut movie", "wut time", "wut can i say", "wut happened"):
            return out("casual_conversation")
        if contains(lowered, "haha", "lol", "lmaoo"):
            return out("humor")
        return out("commenting")

    if word == "zounds":
        if contains(lowered, "zounds hearing announces", "new v.p. of marketing"):
            return out("advertising_spam", "Corporate press-release repost.")
        if contains(lowered, "fallout: new vegas", "trailer"):
            return out("gaming")
        if contains(lowered, "philip catherine", "peace punk records"):
            return out("music_discussion")
        if "http" in lowered and contains(lowered, "new blog post", "northjersey", "msnbc article", "movie in history", "twitpic", "paleofuture", "tinyurl"):
            return out("article_sharing")
        if contains(lowered, "kimiko date krumm", "auckland"):
            return out("sports_discussion")
        if contains(lowered, "oo thats zounds great", "@loveheroes"):
            return out("casual_conversation")
        if contains(lowered, "zounds!") and ("@" not in text) and not "http" in lowered:
            return out("reaction")
        if contains(lowered, "man! this is brilliant", "your turn: go! write!", "vintagewordupgrade", "sexually attractive derogatory term"):
            return out("humor")
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
    reaction_path = BATCH_DIR / "reaction.csv"
    approval_path = BATCH_DIR / "approval.csv"

    reaction_rows = load_csv(reaction_path)
    for row in reaction_rows:
        context, ironic, note = classify_reaction(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    reaction_overrides = {
        "7451322158": "storytelling",
        "7575718877": "criticism",
        "7757239303": "sports_discussion",
        "8102491670": "commenting",
        "8971470601": "humor",
        "8988870480": "casual_conversation",
        "9246610044": "music_discussion",
        "9246627076": "advertising_spam",
        "9307908872": "dating_context",
        "9307915407": "casual_conversation",
        "9736306895": "news_reaction",
        "10095517662": "compliment",
        "10095529626": "compliment",
        "10331677435": "commenting",
        "10385497539": "news_reaction",
        "10385499311": "self_description",
        "12131475175": "food_related",
        "12631025981": "article_sharing",
        "12631200398": "music_discussion",
        "12631216159": "music_discussion",
        "13045630290": "advertising_spam",
        "13459283529": "casual_conversation",
        "13498262245": "casual_conversation",
        "13503658701": "casual_conversation",
        "13507015719": "casual_conversation",
        "13792860779": "casual_conversation",
        "13797678716": "technology_discussion",
        "13797712792": "food_related",
        "13798580204": "casual_conversation",
        "13802609082": "casual_conversation",
        "13804379452": "casual_conversation",
        "13806248690": "casual_conversation",
        "13808585127": "advertising_spam",
        "13934101765": "casual_conversation",
        "13944230691": "casual_conversation",
        "13944928183": "technology_discussion",
        "13945028755": "technology_discussion",
        "13945418842": "casual_conversation",
        "13945589154": "compliment",
        "13947037629": "casual_conversation",
        "14197214876": "sports_discussion",
        "14238020414": "storytelling",
        "14410953969": "television_reference",
        "14459217020": "celebrity_gossip",
        "14541883061": "casual_conversation",
        "14744924506": "casual_conversation",
        "14874777470": "casual_conversation",
        "15992029343387648": "storytelling",
        "17986503805": "self_description",
        "19070062325407744": "commenting",
        "19349353640": "work_school",
        "19361579183": "humor",
        "20151976609": "news_reaction",
        "20581249983": "commenting",
        "22088980332": "humor",
        "22183722783": "storytelling",
        "29354835820": "storytelling",
        "4645850756157440": "work_school",
        "9316900190294016": "music_discussion",
        "14183418183024640": "music_discussion",
        "15520875407220736": "technology_discussion",
        "15522794083196928": "technology_discussion",
        "15600152114888704": "technology_discussion",
        "7650158361": "advertising_spam",
        "7651011850": "advertising_spam",
        "7651030357": "advertising_spam",
        "7651827644": "advertising_spam",
        "22140352602": "sports_discussion",
        "22140385536": "sports_discussion",
    }
    apply_overrides(reaction_rows, reaction_overrides, "Reaction review override: ")

    approval_rows = load_csv(approval_path)
    approval_overrides = {
        "7849430206": "self_description",
        "10799830846": "food_related",
        "11447207762": "fashion_beauty",
        "18059759630": "compliment",
        "22432430878": "article_sharing",
        "10304265029": "food_related",
        "12181631298": "television_reference",
        "15971616952": "gaming",
        "18389061671": "gaming",
        "19368161082": "food_related",
    }
    apply_overrides(approval_rows, approval_overrides, "Darwin audit: ")

    irony_updates = {
        "25888407537": ("true", "Comic exaggeration about a 'bomb ass dream'."),
        "5317465001168896": ("true", "Explicit 'HAHA JKJK' marks joking/nonliteral praise."),
        "8971470601": ("true", "Playful incredulous humor signaled by Lol and baha."),
        "14238020414": ("true", "Hahahaha plus 'dafuq?' is clearly joking disbelief."),
        "14409354110": ("true", "LMFAO plus exaggerated snake reaction is overtly comic."),
        "19361579183": ("true", "Lmao plus 'Dafuq?' is humorous disbelief."),
        "22088980332": ("true", "haha dafuq!? is clear playful incredulity."),
        "9092588160": ("true", "lol *gag* is performative mock disgust."),
        "9555722291": ("true", "making me gag ... LOL is comic exaggeration."),
    }
    apply_irony_updates(
        {"approval": approval_rows, "reaction": reaction_rows},
        irony_updates,
    )

    write_csv(reaction_path, reaction_rows)
    write_csv(approval_path, approval_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (reaction_rows, approval_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("reaction_contexts", Counter(row["usage_context"] for row in reaction_rows).most_common())
    print("reaction_irony", Counter(row["is_ironic"] for row in reaction_rows).most_common())
    print("approval_irony", Counter(row["is_ironic"] for row in approval_rows).most_common())


if __name__ == "__main__":
    main()
