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


def classify_social(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "BFFL":
        if contains(lowered, "justin bieber", "nickjonas", "demi lovato", "cody simpson", "muchmusic", "buffalo"):
            return out("celebrity_gossip")
        if contains(lowered, "new video", "reverbnation", "unplugged in studio"):
            return out("music_discussion")
        if contains(lowered, "theme park", "big five for life", "stardoll", "go follow", "few tickets still"):
            return out("advertising_spam")
        if contains(lowered, "school", "skool", "baseball game", "presentation", "homework"):
            return out("work_school")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "happy 21st", "congrats", "super late"):
            return out("compliment")
        return out("casual_conversation")

    if word == "F2F":
        if contains(lowered, "#followforfollow", "#follow4follow", "#followback"):
            return out("advertising_spam")
        if contains(lowered, "exam", "forms,follow-ups", "time off work", "work off their plate", "discussion forum", "faculty focus", "#elearning", "college", "presentation", "homework"):
            return out("work_school")
        if contains(lowered, "nfl teams", "draft"):
            return out("sports_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "GLHF":
        if contains(lowered, "halo wars", "tekken", "street fighter", "lan party", "ghost stories team", "glhf.it", "gosugamers", "starcraft", "glhf.tv", "tournament", "monday night combat"):
            return out("gaming")
        if contains(lowered, "school starts", "college starts", "presentation", "homework"):
            return out("work_school")
        if contains(lowered, "buy tickets now", "flashmob", "what r u waitin' for"):
            return out("advertising_spam")
        if contains(lowered, "olympic games", "opening tonite"):
            return out("sports_discussion")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "bro":
        if contains(lowered, "big bro", "jonas"):
            return out("television_reference" if "big bro" in lowered else "music_discussion")
        if contains(lowered, "mixtape", "#nowplaying", "album", "track", "workout", "diddy", "last train to paris"):
            return out("music_discussion")
        if contains(lowered, "#followfriday", "plz rt", "follow my bro"):
            return out("advertising_spam")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "bromance":
        if contains(lowered, "tim berg", "avicii", "seek bromance", "bad bromance", "#nowplaying", "arena mix"):
            return out("music_discussion")
        if contains(lowered, "jude law", "robert downey", "snl", "tebow", "mccoy", "bernancke", "saban"):
            return out("celebrity_gossip")
        if contains(lowered, "album review", "true bromance ep"):
            return out("article_sharing")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "dis":
        if contains(lowered, "loving dis song", "video", "watchin dis plies video"):
            return out("music_discussion")
        if contains(lowered, "smells like mad food", "cravinq"):
            return out("food_related")
        if contains(lowered, "song for yu", "rihanna's army", "that's funny"):
            return out("commenting")
        if contains(lowered, "class", "school"):
            return out("work_school")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "dogg":
        if contains(lowered, "snoop dogg", "tha dogg pound", "#nowplaying", "money over here", "i wanna rock"):
            return out("music_discussion")
        if contains(lowered, "gamertag", "what games"):
            return out("gaming")
        if contains(lowered, "hot dogg'd", "pizza'd"):
            return out("humor")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "ent":
        if contains(lowered, "ent associates", "job on", "#immunologist-us"):
            return out("advertising_spam")
        if contains(lowered, "nexus one enterprise version", "enterprise version"):
            return out("technology_discussion")
        if contains(lowered, "new video", "youtube", "hiphopconfession", "bangkok ent", "gucciboys", "fullsail"):
            return out("music_discussion")
        if contains(lowered, "i ent", "ent coming out", "wud love an ent. version", "beat team"):
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "lemme":
        if contains(lowered, "myspace", "music", "song", "youtube"):
            return out("music_discussion")
        if contains(lowered, "lemme touch you please", "pop that pussy", "#norape"):
            return out("sexual_context")
        if contains(lowered, "sunday world"):
            return out("article_sharing")
        if contains(lowered, "breakfast", "workin again", "work"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "okee-doke":
        if contains(lowered, "fell for the okee doke", "jets"):
            return out("sports_discussion")
        if contains(lowered, "off to class"):
            return out("work_school")
        if contains(lowered, "tariq alexander", "video", "youtube"):
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "peeps":
        if contains(lowered, "calculator app", "test & maybe give word of mouth adv", "go add peeps from my followers", "followers yo"):
            return out("advertising_spam")
        if contains(lowered, "work tomorrow", "working for a couple days"):
            return out("work_school")
        if contains(lowered, "beautiful peeps"):
            return out("compliment")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "sesh":
        if contains(lowered, "surf sesh", "sk8park", "swim sesh", "gym sesh", "workout"):
            return out("sports_discussion")
        if contains(lowered, "jam sesh", "norma jean", "video sesh", "monstro_band", "pianooooo"):
            return out("music_discussion")
        if contains(lowered, "beauty sesh"):
            return out("fashion_beauty")
        if contains(lowered, "work sesh"):
            return out("work_school")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "sinse":
        if contains(lowered, "skool", "school", "video shoot", "beat", "sonar", "tutorials"):
            return out("work_school" if contains(lowered, "skool", "school") else "music_discussion")
        if contains(lowered, "twitter", "twlol.com", "#lol", "#ichc"):
            return out("article_sharing")
        if contains(lowered, "i could still get a man", "janet showed her titty"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "sis":
        if contains(lowered, "@ddlovato", "madison", "great actress"):
            return out("celebrity_gossip")
        if contains(lowered, "do my hw", "work today"):
            return out("work_school")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    if word == "sport":
        if contains(lowered, "jeep wrangler sport", "sport crew socks"):
            return out("advertising_spam")
        if "http" in lowered:
            return out("article_sharing")
        return out("sports_discussion")

    if word == "whadja":
        if contains(lowered, "computer", "setting up"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("casual_conversation")

    return out("casual_conversation")


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
    social_path = BATCH_DIR / "social.csv"
    insult_path = BATCH_DIR / "insult.csv"

    social_rows = load_csv(social_path)
    for row in social_rows:
        context, ironic, note = classify_social(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    social_overrides = {
        "7310123266": "celebrity_gossip",
        "7310370566": "celebrity_gossip",
        "7334416702": "work_school",
        "7337456534": "advertising_spam",
        "7480009961": "work_school",
        "7516545080": "work_school",
        "7519630199": "work_school",
        "7695184894": "work_school",
        "7696235871": "music_discussion",
        "7728356697": "gaming",
        "7895169972": "work_school",
        "7914751081": "advertising_spam",
        "7915378769": "advertising_spam",
        "8330932247": "advertising_spam",
        "8421892656": "music_discussion",
        "8568891037": "advertising_spam",
        "8595255620": "advertising_spam",
        "8833053941": "sports_discussion",
        "8833843750": "work_school",
        "8927190279": "article_sharing",
        "8944423096": "work_school",
        "8998850135": "compliment",
        "9001924652": "sports_discussion",
        "9424052043": "celebrity_gossip",
        "9696235871": "music_discussion",
        "9696981191": "work_school",
        "9962690526": "celebrity_gossip",
        "10022523268": "advertising_spam",
        "10083950527": "advertising_spam",
        "10150163673": "music_discussion",
        "10180550653": "celebrity_gossip",
        "10180865439": "celebrity_gossip",
        "10217119761": "self_description",
        "10217202198": "advertising_spam",
        "10217202867": "advertising_spam",
        "10348757593": "television_reference",
        "10643059840": "music_discussion",
        "10658531440": "music_discussion",
        "10998631739": "advertising_spam",
        "10998716385": "advertising_spam",
        "10998801526": "advertising_spam",
        "10998806688": "advertising_spam",
        "10998914800": "advertising_spam",
        "10999024745": "advertising_spam",
        "10999037458": "advertising_spam",
        "11584933400": "gaming",
        "11588385313": "music_discussion",
        "12010614490": "work_school",
        "12015247100": "advertising_spam",
        "12442709147": "music_discussion",
        "12445944929": "advertising_spam",
        "12446014168": "advertising_spam",
        "12446108182": "advertising_spam",
        "12433014394978304": "food_related",
        "12530760112": "sports_discussion",
        "12723836038414336": "music_discussion",
        "13171985000": "music_discussion",
        "13507596146": "gaming",
        "14033282163": "self_description",
        "14034349941": "advertising_spam",
        "14035751659": "advertising_spam",
        "14572522630": "music_discussion",
        "14989306648": "gaming",
        "15020959622758400": "music_discussion",
        "15159151281840128": "advertising_spam",
        "15163645965115392": "advertising_spam",
        "15167020517560320": "advertising_spam",
        "15167329671319552": "advertising_spam",
        "16389349243": "music_discussion",
        "16486822047": "work_school",
        "16488525599": "advertising_spam",
        "17336658914": "work_school",
        "18247512317": "music_discussion",
        "18273609621": "article_sharing",
        "18342215902": "work_school",
        "18847075552": "gaming",
        "18898824638": "celebrity_gossip",
        "18899094283": "celebrity_gossip",
        "20894747824": "gaming",
        "20910442396": "gaming",
        "21083419803": "gaming",
        "21229378529": "advertising_spam",
        "22580616257": "work_school",
        "22582151427": "advertising_spam",
        "22998539893": "sports_discussion",
        "23910357406": "advertising_spam",
        "24264396614": "advertising_spam",
        "24264571257": "advertising_spam",
        "25154996813": "work_school",
        "26539584217": "compliment",
        "27399521502": "commenting",
        "27399606674": "advertising_spam",
        "28011349940": "music_discussion",
        "29167028651": "article_sharing",
        "3079376681832448": "work_school",
        "3079462337908736": "self_description",
        "1137008181248001": "music_discussion",
        "1140748791582720": "advertising_spam",
        "1223505567817728": "compliment",
        "7230166648492032": "advertising_spam",
    }
    apply_overrides(social_rows, social_overrides, "Social review override: ")

    insult_rows = load_csv(insult_path)
    insult_overrides = {
        "7381176035": "criticism",
        "7381272839": "criticism",
        "11723005689": "commenting",
        "14373134892": "criticism",
        "15934131581": "criticism",
        "24121284029": "self_description",
        "24729740730": "self_description",
        "27618672241": "self_description",
        "28598166706": "humor",
        "21338074533330944": "criticism",
    }
    apply_overrides(insult_rows, insult_overrides, "Darwin audit: ")

    irony_updates = {
        "20909168221": ("true", "Old-person voice / hearing-aid bit is clear parody."),
        "5992291407761408": ("true", "Explicit JK makes the line clearly joking."),
        "15264607467": ("true", "Tweet explicitly says the speaker is joking."),
    }
    apply_irony_updates({"social": social_rows, "insult": insult_rows}, irony_updates)

    write_csv(social_path, social_rows)
    write_csv(insult_path, insult_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (social_rows, insult_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("social_contexts", Counter(row["usage_context"] for row in social_rows).most_common())
    print("social_irony", Counter(row["is_ironic"] for row in social_rows).most_common())
    print("insult_contexts", Counter(row["usage_context"] for row in insult_rows).most_common())


if __name__ == "__main__":
    main()
