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


def classify_description(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "AWOL":
        if contains(lowered, "windows 7 boot camp awol", "boot camp awol"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "phone is awol", "twitfam has went awol", "you went awol", "bestfriend is awol"):
            return out("casual_conversation")
        return out("commenting")

    if word == "TBA":
        if contains(lowered, "call of duty", "title tba"):
            return out("gaming")
        if contains(lowered, "job:", "senior mechanical engineer", "salary tba"):
            return out("advertising_spam")
        if contains(lowered, "espn2:", "spring football", "times tba"):
            return out("sports_discussion")
        if contains(lowered, "new song", "trance cd project", "hula grill", "live music by"):
            return out("music_discussion")
        if contains(lowered, "@") and not "http" in lowered:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "a-list":
        if contains(lowered, "radio 2's a-list", "a-list radio"):
            return out("music_discussion")
        if contains(lowered, "come party", "a-list tues", "ladies free", "guest list", "just say mch"):
            return out("advertising_spam")
        if contains(lowered, "a-list celebs", "wwe wrestler", "movie", "tv"):
            return out("celebrity_gossip")
        if contains(lowered, "a-list card", "model for you guys"):
            return out("fashion_beauty")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "annihilated":
        if contains(lowered, "cupcakes", "temp roll", "noodles"):
            return out("food_related")
        if contains(lowered, "#ravens", "pats", "packers"):
            return out("sports_discussion")
        if contains(lowered, "u.n. should be annihilated", "club for dictators"):
            return out("criticism")
        if contains(lowered, "game", "annihilated with me"):
            return out("casual_conversation")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "badass":
        if contains(lowered, "movie", "matt damon", "brothers was a badass movie"):
            return out("television_reference")
        if contains(lowered, "attorney of the week", "sues bank of america"):
            return out("article_sharing")
        if contains(lowered, "game! go cards", "badass game"):
            return out("sports_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("compliment")
        return out("compliment")

    if word == "blankie":
        if contains(lowered, "teether blankie", "baby product", "toys"):
            return out("advertising_spam")
        if contains(lowered, "fringe", "american idol"):
            return out("television_reference")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "wish i could snuggle", "get cozy", "need my blankie", "house so cold", "blankie now"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "bowl":
        if contains(lowered, "rose bowl", "sugar bowl", "gator bowl", "pro bowl", "cotton bowl"):
            return out("sports_discussion")
        if contains(lowered, "plastic bowl", "bowl of vanilla gelato", "bowl of popcorn"):
            return out("food_related")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "bumfuck":
        if contains(lowered, "middle of bumfuck", "bumfuck ohio", "bumfuck egypt", "bumfuck central"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "compo":
        if contains(lowered, "competition", "compo"):
            return out("commenting")
        if contains(lowered, "job", "cv", "folio", "portfolio"):
            return out("work_school")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "crappy":
        if contains(lowered, "movie", "tv", "job", "work", "show"):
            return out("commenting")
        if contains(lowered, "i feel crappy", "today is crappy"):
            return out("self_description")
        if contains(lowered, "food", "ate", "burger", "meal"):
            return out("food_related")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "flutterby":
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "flutterby beauty", "flutterby creations"):
            return out("advertising_spam")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "gnarly":
        if contains(lowered, "video", "tv", "movie"):
            return out("television_reference")
        if contains(lowered, "gnarly cold", "gnarly allergies", "gnarly anxiety", "gnarly sunburn"):
            return out("self_description")
        if contains(lowered, "lets get gnarly", "tonight wuz gnarly"):
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "gridlock":
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "traffic", "stuck in", "commute"):
            return out("self_description")
        return out("news_reaction" if contains(lowered, "news", "crisis") else "commenting")

    if word == "horribad":
        if contains(lowered, "game", "movie", "song"):
            return out("commenting")
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "jalopy":
        if contains(lowered, "car", "jeep", "drive"):
            return out("commenting")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "pregos":
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if contains(lowered, "pregnant", "pregos"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "preemie":
        if contains(lowered, "nicu", "baby", "premature"):
            return out("commenting")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "rachet":
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if contains(lowered, "school", "class"):
            return out("work_school")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "shiesty":
        if contains(lowered, "lol", "lmao", "haha"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "sicc":
        if contains(lowered, "tonsils", "fever", "church", "can't afford to be sicc", "i sicc"):
            return out("self_description")
        if contains(lowered, "flow madd sicc", "givens aint sicc"):
            return out("compliment")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "skeevy":
        if contains(lowered, "follower", "fb", "myspace", "actor", "cat-call"):
            return out("commenting")
        if contains(lowered, "i feel very uncomfortable", "too skeevy"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "skyrocket":
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "ratings skyrocket", "tweet count skyrocket", "food prices skyrocket"):
            return out("news_reaction")
        if contains(lowered, "hope you just skyrocket"):
            return out("compliment")
        return out("commenting")

    if word == "streak":
        if contains(lowered, "dell's 'streak' slate", "#tech", "ces 2010"):
            return out("technology_discussion")
        if contains(lowered, "xbox live streak", "achievement tutorial"):
            return out("gaming")
        if contains(lowered, "win streak", "state ends northern iowa's win streak", "run streak"):
            return out("sports_discussion")
        if contains(lowered, "purple streak", "blue streak"):
            return out("appearance")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "sucky":
        if contains(lowered, "birthday", "year", "day", "grades", "tomorrow"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "thingamabob":
        if contains(lowered, "zune", "geo tag", "identica", "ups thingamabob", "virus thingamabob"):
            return out("technology_discussion")
        if contains(lowered, "class", "project"):
            return out("work_school")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "zombie":
        if contains(lowered, "rob zombie", "bubblegum", "octane"):
            return out("music_discussion")
        if contains(lowered, "map", "zombie maps", "vampire penguins? zombie guinea pigs?"):
            return out("gaming")
        if contains(lowered, "rom-com", "halloween ii", "zombie boyfriend", "zombie movie"):
            return out("television_reference")
        if contains(lowered, "zombie apocalypse", "zombie survival guide", "zombie gingerbread house"):
            return out("humor")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "zooted":
        if contains(lowered, "mary jane", "session", "lab chillin", "mixtape joints"):
            return out("drug_context")
        if contains(lowered, "burger king", "funnel cake sticks", "choco puffs", "golden grams", "coffee", "starbucks"):
            return out("food_related")
        if contains(lowered, "among the thirsty", "song", "video"):
            return out("music_discussion")
        if contains(lowered, "watchin tv", "movie", "#tvflow"):
            return out("television_reference")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

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
    description_path = BATCH_DIR / "description.csv"
    behavior_path = BATCH_DIR / "behavior.csv"

    description_rows = load_csv(description_path)
    for row in description_rows:
        context, ironic, note = classify_description(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    description_overrides = {
        "7295638124": "sports_discussion",
        "7297002884": "casual_conversation",
        "7297962584": "gaming",
        "7298574493": "advertising_spam",
        "7310761164": "article_sharing",
        "7311454089": "technology_discussion",
        "7394364173": "advertising_spam",
        "7395235907": "advertising_spam",
        "7395581317": "advertising_spam",
        "7395811627": "advertising_spam",
        "7396513026": "advertising_spam",
        "7415513541": "music_discussion",
        "7415922827": "music_discussion",
        "7415954887": "advertising_spam",
        "7415986163": "advertising_spam",
        "7416753956": "music_discussion",
        "7420307667": "sports_discussion",
        "7511221785": "article_sharing",
        "7516580306": "commenting",
        "7532942170": "article_sharing",
        "7535129313": "news_reaction",
        "7690299897": "advertising_spam",
        "7757659985": "casual_conversation",
        "7758226373": "casual_conversation",
        "7759178613": "technology_discussion",
        "7948028545": "advertising_spam",
        "7977134954": "gaming",
        "8379240584": "music_discussion",
        "8379313897": "technology_discussion",
        "8379790059": "technology_discussion",
        "8380092679": "technology_discussion",
        "8400515547": "advertising_spam",
        "8401046137": "technology_discussion",
        "8401171348": "technology_discussion",
        "8406941260": "technology_discussion",
        "8656958312": "humor",
        "9837361911": "advertising_spam",
        "9838522387": "technology_discussion",
        "9913817024": "advertising_spam",
        "9915248844": "advertising_spam",
        "9915649222": "advertising_spam",
        "9915753605": "advertising_spam",
        "9915961600": "sports_discussion",
        "10065786086": "advertising_spam",
        "10782379086": "music_discussion",
        "10787749052": "self_description",
        "10784078210": "sports_discussion",
        "10891342087": "advertising_spam",
        "10892171324": "advertising_spam",
        "10892441461": "advertising_spam",
        "10892610935": "advertising_spam",
        "10892611279": "advertising_spam",
        "11241930431": "advertising_spam",
        "11243722268": "music_discussion",
        "11243813875": "music_discussion",
        "11536141565": "advertising_spam",
        "12371718995": "technology_discussion",
        "12625482111": "music_discussion",
        "12627407183": "advertising_spam",
        "14955094030": "sports_discussion",
        "15458255255": "advertising_spam",
        "17625910225": "sports_discussion",
        "18273609621": "article_sharing",
        "18927430917": "advertising_spam",
        "18928564882": "advertising_spam",
        "20582791415": "advertising_spam",
        "20584896012": "advertising_spam",
        "20585187582": "advertising_spam",
        "14737965292978176": "self_description",
    }
    apply_overrides(description_rows, description_overrides, "Description review override: ")

    behavior_rows = load_csv(behavior_path)
    behavior_overrides = {
        "8570694287": "sports_discussion",
        "10201581622": "self_description",
        "11112530842": "food_related",
        "12297870898": "self_description",
        "12676399952": "sports_discussion",
        "12699825694": "article_sharing",
        "12700080598": "article_sharing",
    }
    apply_overrides(behavior_rows, behavior_overrides, "Darwin audit: ")

    irony_updates = {
        "13355562321": ("true", "Tweet explicitly says a 'jk' was added, so tone is joking."),
        "8656958312": ("true", "Zombie apocalypse hypothetical plus FML LOL is clearly nonliteral."),
        "14737965292978176": ("true", "`#winningtweet` plus Lmao frames `#zooted everyday` as playful exaggeration."),
    }
    apply_irony_updates({"behavior": behavior_rows, "description": description_rows}, irony_updates)

    write_csv(description_path, description_rows)
    write_csv(behavior_path, behavior_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (description_rows, behavior_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("description_contexts", Counter(row["usage_context"] for row in description_rows).most_common())
    print("description_irony", Counter(row["is_ironic"] for row in description_rows).most_common())
    print("behavior_irony", Counter(row["is_ironic"] for row in behavior_rows).most_common())


if __name__ == "__main__":
    main()
