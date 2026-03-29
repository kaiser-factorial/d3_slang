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


def classify_behavior(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "CBA":
        if contains(lowered, "christian brothers academy", "mls cba", "collective bargaining agreement", "#football", "#arsenal", "sounders"):
            return out("sports_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "work", "essay", "english", "ballet", "ict", "sleep", "phone would stop ringing"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "chillax":
        if contains(lowered, "apply for ben cheney", "cullensonline.com"):
            return out("advertising_spam")
        if contains(lowered, "work told me", "homework", "grind begins again", "review"):
            return out("work_school")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "fap":
        if contains(lowered, "fap turbo", "forex robot", "download for free"):
            return out("advertising_spam")
        if contains(lowered, "#fap", "xtube", "fap on the cover", "make you fap", "reason to fap"):
            return out("sexual_context")
        if contains(lowered, "@fap_girl"):
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("sexual_context")

    if word == "gotsta":
        if contains(lowered, "go to work", "open in the morn", "sleep", "do better in this twitter world"):
            return out("self_description")
        if contains(lowered, "car prison", "stationed in jersey city", "music ur pen"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "hypermiler":
        if contains(lowered, "#hypermiling", "insight", "epa rating", "prius", "eco-drive"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "mosey":
        if contains(lowered, "customer service forum", "reboot cenarius"):
            return out("gaming")
        if contains(lowered, "roger mosey", "london 2012", "#olympics"):
            return out("sports_discussion")
        if contains(lowered, "office", "class", "kitchen", "bed", "coffee", "times square"):
            return out("self_description")
        if contains(lowered, "e-how", "social site", "helpful folks", "articles"):
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "plastered":
        if contains(lowered, "billboard campaign", "desktop", "shelves", "snow", "desk plastered", "mugs for sale", "coffee mugs"):
            return out("commenting")
        if contains(lowered, "getting plastered", "few make", "propose while plastered", "is getting plastered"):
            return out("self_description")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("self_description")

    if word == "rehab":
        if contains(lowered, "registered nurse acute rehab", "rehab therapy", "rehab mgr", "#jobs", "emory healthcare", "kindred healthcare"):
            return out("work_school")
        if contains(lowered, "celeb rehab", "tiger woods", "amy winehouse", "#nowplaying"):
            return out("celebrity_gossip" if "tiger woods" in lowered or "celeb rehab" in lowered else "music_discussion")
        if contains(lowered, "rehab for twitter", "twitter rehab", "fapper rehab"):
            return out("humor")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "revert":
        if contains(lowered, "email:", "please check ur mail", "revert me back", "budget/requirement", "mail us"):
            return out("work_school")
        if contains(lowered, "dom tree", "bugfix", "email footer", "headphones or speakers", "sound settings"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "sleep schedule", "revert back", "old happy books", "being a b*tch"):
            return out("self_description")
        return out("commenting")

    if word == "soused":
        if contains(lowered, "fruit cake", "soused cherries", "foie gras"):
            return out("food_related")
        if contains(lowered, "song of the soused"):
            return out("music_discussion")
        if contains(lowered, "drinking game", "soused spouse", "get her soused", "she was definitely soused", "soused haze", "soused five minutes in"):
            return out("commenting")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "thirsty":
        if contains(lowered, "water", "drink", "beer wagon", "glasses of water", "still so thirsty"):
            return out("self_description")
        if contains(lowered, "patty mayonnaise", "thirsty nigga", "thirsty bitches", "aggressiveness", "#thirsty"):
            return out("commenting")
        if contains(lowered, "among the thirsty", "need a savior", "video"):
            return out("music_discussion")
        if contains(lowered, "youtube", "twitpic") and "http" in lowered:
            return out("article_sharing")
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
    behavior_path = BATCH_DIR / "behavior.csv"
    social_path = BATCH_DIR / "social.csv"

    behavior_rows = load_csv(behavior_path)
    for row in behavior_rows:
        context, ironic, note = classify_behavior(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    behavior_overrides = {
        "7979527651": "sports_discussion",
        "8065593982": "work_school",
        "8065633510": "work_school",
        "8137368786": "sports_discussion",
        "8137588425": "article_sharing",
        "8137589030": "article_sharing",
        "8137692877": "article_sharing",
        "8137713289": "article_sharing",
        "8344829458": "humor",
        "8344920138": "humor",
        "8344997040": "humor",
        "8570033314": "advertising_spam",
        "8570412129": "article_sharing",
        "8571441308": "sports_discussion",
        "8572207077": "sports_discussion",
        "8587913523": "sports_discussion",
        "8587917578": "technology_discussion",
        "8588130776": "article_sharing",
        "8770200775": "article_sharing",
        "8770234691": "sports_discussion",
        "8822203579": "article_sharing",
        "8822294371": "article_sharing",
        "8903974336": "article_sharing",
        "8905208616": "article_sharing",
        "8978464970": "article_sharing",
        "8978506883": "article_sharing",
        "9218472734": "sports_discussion",
        "9218508645": "music_discussion",
        "9490631488": "humor",
        "9490652617": "technology_discussion",
        "9591361942": "news_reaction",
        "9591364252": "technology_discussion",
        "9591417222": "work_school",
        "10200671886": "advertising_spam",
        "10201581622": "article_sharing",
        "10201772563": "article_sharing",
        "10202528810": "commenting",
        "10202867774": "advertising_spam",
        "10508066096": "article_sharing",
        "10864251721": "article_sharing",
        "10864260399": "article_sharing",
        "10864290559": "article_sharing",
        "12063241298": "advertising_spam",
        "12149339592": "advertising_spam",
        "12149765941": "sports_discussion",
        "12199610715": "technology_discussion",
        "12678170478": "advertising_spam",
        "12678468874": "advertising_spam",
        "12679450740": "sports_discussion",
        "12682127861": "article_sharing",
        "12698791876": "advertising_spam",
        "12698809375": "advertising_spam",
        "12698814163": "advertising_spam",
        "12698818743": "advertising_spam",
        "12699825694": "technology_discussion",
        "12700080598": "technology_discussion",
        "13452076251": "sports_discussion",
        "13452673916": "technology_discussion",
        "13575198901": "commenting",
        "14391773235": "sports_discussion",
        "14392051545": "sports_discussion",
        "14392795830": "gaming",
        "15740054989": "sports_discussion",
        "17326923747": "advertising_spam",
        "18562086218": "humor",
        "23007413958": "humor",
        "24846303091": "advertising_spam",
        "25519161380": "advertising_spam",
        "26802850216": "casual_conversation",
        "4545502003593216": "article_sharing",
        "4548553443639296": "sports_discussion",
        "4775911312326656": "commenting",
        "7285451144560640": "humor",
        "9610142702108672": "sports_discussion",
    }
    apply_overrides(behavior_rows, behavior_overrides, "Behavior review override: ")

    social_rows = load_csv(social_path)
    social_overrides = {
        "7310123266": "casual_conversation",
        "7310370566": "casual_conversation",
        "9424052043": "casual_conversation",
        "9962690526": "casual_conversation",
        "12010614490": "casual_conversation",
        "12445944929": "advertising_spam",
        "12446014168": "advertising_spam",
        "15725009311": "casual_conversation",
        "20259061294": "criticism",
        "22631268863": "music_discussion",
    }
    apply_overrides(social_rows, social_overrides, "Darwin audit: ")

    irony_updates = {
        "13820440279523328": ("true", "`loljk` explicitly marks the line as joking."),
        "11843753077637120": ("true", "`haha jk` makes the threat clearly playful."),
        "18562086218": ("true", "`Rehab is for quitters` is overt humorous nonliteral phrasing."),
        "23007413958": ("true", "Extended love-as-drug metaphor is clearly nonliteral."),
        "7285451144560640": ("true", "Exaggerated prediction plus mahahaha is overtly mocking."),
        "26802850216": ("true", "`#soused jk` explicitly signals joking use."),
        "4775911312326656": ("true", "`Lol j/p` marks the #thirsty label as a joke."),
    }
    apply_irony_updates({"social": social_rows, "behavior": behavior_rows}, irony_updates)

    write_csv(behavior_path, behavior_rows)
    write_csv(social_path, social_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (behavior_rows, social_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("behavior_contexts", Counter(row["usage_context"] for row in behavior_rows).most_common())
    print("behavior_irony", Counter(row["is_ironic"] for row in behavior_rows).most_common())
    print("social_irony", Counter(row["is_ironic"] for row in social_rows).most_common())


if __name__ == "__main__":
    main()
