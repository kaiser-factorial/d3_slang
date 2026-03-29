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


def classify_technology(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "IBT":
        if contains(lowered, "toefl", "ibt practice", "ibt speaking", "english test"):
            return out("work_school", "TOEFL iBT exam-prep context.")
        if contains(lowered, "@ibluetooth", "bt transfer", "ibluetooth", "ibluetransfer"):
            return out("technology_discussion")
        if "http" in lowered and contains(lowered, "fantasy football", "commodities", "gold bubble", "promo tour"):
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("technology_discussion", "IBT usually functions as a tech/app acronym in this batch.")

    if word == "SWF":
        if contains(lowered, "job:", "freelance", "virtual asst.", "redesign flash swf", "simple redesign"):
            return out("advertising_spam")
        if contains(lowered, "convert swf", "flash(.swf)", "animation from swf", "type “swf”", "image viewer xml", "playback on ipod", "iphone,psp"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing", "Linked SWF file/demo/tutorial share.")
        if contains(lowered, "can anyone help", "struggling to convert", "flash for phones"):
            return out("technology_discussion")
        return out("technology_discussion")

    if word == "compy":
        if contains(lowered, "classes", "homework", "notes", "reading", "drivers on compy"):
            return out("work_school")
        if contains(lowered, "#nowplaying", "favorite song", "albums cause i cant re-download them"):
            return out("music_discussion")
        if contains(lowered, "zelda", "movie on my compy"):
            return out("gaming" if "zelda" in lowered else "commenting")
        if contains(lowered, "looking 4 a network engineer guru", "dot.com compy"):
            return out("advertising_spam")
        if contains(lowered, "taking a break from compy", "just woke up ah so compy in bed", "the longer i spend on compy", "i havent been on my compy", "new compy", "bought a new compy"):
            return out("self_description")
        if "@" in text:
            return out("casual_conversation")
        return out("technology_discussion")

    if word == "crossfade":
        if contains(lowered, "crossfade -", "#nowlistening", "listening to", "great tune", "crossfade_sfl"):
            return out("music_discussion")
        if contains(lowered, "ultra music festival", "miaminewtimes.com/crossfade", "v-moda crossfade"):
            return out("article_sharing")
        if contains(lowered, "spotify", "crossfade optomisation", "mix, and not just crossfade"):
            return out("technology_discussion")
        if "@" in text:
            return out("casual_conversation")
        return out("music_discussion", "Band/title use dominates this term.")

    if word == "crowdsourcing":
        if contains(lowered, "shorty award", "@utest", "@innocentive", "meetup tomorrow", "unconference"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("commenting")
        return out("technology_discussion")

    if word == "nuker":
        if contains(lowered, "work nuker", "blackened nuker"):
            return out("food_related", "Microwave use, not software slang.")
        if contains(lowered, "spyware nuker", "error nuker", "evidencenuker", "seo nuker"):
            return out("advertising_spam")
        if contains(lowered, "9dragons", "grinding", "best of cl vote"):
            return out("gaming" if "9dragons" in lowered else "commenting")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("technology_discussion")

    if word == "spam":
        if contains(lowered, "spam musubi", "maruki tei"):
            return out("food_related")
        if contains(lowered, "banelings evolve", "spam them"):
            return out("gaming")
        if contains(lowered, "spam him this link", "spam it plzzz", "new celly need new"):
            return out("advertising_spam")
        if contains(lowered, "spam list", "spam email", "spam emails", "social media spam", "scam/spam", "phishing", "spam this week"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "spec":
        if contains(lowered, "spec ops", "modern warfare 2", "breach&clear"):
            return out("gaming")
        if contains(lowered, "formal grammar spec", "img tag", "defined format in the spec"):
            return out("technology_discussion")
        if contains(lowered, "spec boogie", "von pea", "album: heartbreak city"):
            return out("music_discussion")
        if contains(lowered, "job description", "billing - columbus", "clin nurse spec", "pilot re-certification assistance"):
            return out("advertising_spam")
        if contains(lowered, "spec interest", "body-kit", "a spec rear"):
            return out("article_sharing")
        if contains(lowered, "cavs showed", "lakers"):
            return out("sports_discussion")
        if contains(lowered, "happy bday spec", "i miss u spec"):
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "spec-ops":
        if contains(lowered, "mw2", "modern warfare", "achievements", "video guide", "session", "veteran"):
            return out("gaming")
        if contains(lowered, "just listed:", "brand-", "made in the usa", "mag pouch", "phone holster", "knife sheath", "patrol sling", "recon wrap"):
            return out("advertising_spam")
        if "http" in lowered:
            return out("article_sharing")
        return out("technology_discussion")

    if word == "twit":
        if contains(lowered, "twit.tv", "windows weekly", "the tech guy", "twit app", "twit pic"):
            return out("technology_discussion")
        if contains(lowered, "send a twit pic"):
            return out("casual_conversation")
        if contains(lowered, "twit more", "tweet or twit", "twit/tweet using my mobile", "twit world", "twit for tat", "twit krew"):
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("technology_discussion")

    if word == "walkie":
        if contains(lowered, "dog went out", "out for walkie", "walkie home", "drunkie and walkie"):
            return out("casual_conversation", "Pet/walk phrasing rather than radio tech.")
        if contains(lowered, "for sale", "great x-mas present", "order here", "new cobra", "fisher-price"):
            return out("advertising_spam")
        if contains(lowered, "blackberry does not have walkie-talkie", "appidea", "bluetooth", "nextel walkie talkie phone", "motorola t5420"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "workaround":
        if contains(lowered, "spamassasin bug", "itunes", "browser's dom", "jboss", "#5dmk2", "#firefox", "facebook status - api", "xpsp3", "developer account", "workaround link", "exchange calendar", "word patch"):
            return out("technology_discussion")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "don't lose hope yet", "there's usually a workaround", "@"):
            return out("casual_conversation")
        return out("technology_discussion")

    return out("technology_discussion")


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
    technology_path = BATCH_DIR / "technology.csv"
    reaction_path = BATCH_DIR / "reaction.csv"

    technology_rows = load_csv(technology_path)
    for row in technology_rows:
        context, ironic, note = classify_technology(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    technology_overrides = {
        "7317813112": "self_description",
        "7330741517": "self_description",
        "7377333754": "casual_conversation",
        "7377351125": "self_description",
        "7385279902": "advertising_spam",
        "8229857699": "self_description",
        "8232404128": "work_school",
        "8520283935": "music_discussion",
        "11151097468": "self_description",
        "11353873923": "storytelling",
        "11496240743": "music_discussion",
        "11498493693": "work_school",
        "11616809434": "music_discussion",
        "11717006546": "commenting",
        "12390298220": "music_discussion",
        "12740574254": "gaming",
        "12800113626": "work_school",
        "13213097846116352": "fashion_beauty",
        "14475594905": "television_reference",
        "14584764213": "television_reference",
        "15913044760": "article_sharing",
        "16425450411": "self_description",
        "16850847614": "casual_conversation",
        "16859613410": "sports_discussion",
        "16860173330": "casual_conversation",
        "17424014452": "gaming",
        "17424955424": "storytelling",
        "18311396897": "music_discussion",
        "18318056199": "work_school",
        "19634520687": "gaming",
        "20157661798": "television_reference",
        "20539876407": "work_school",
        "21768719747": "gaming",
        "21775520709": "commenting",
        "24172916861": "work_school",
        "24181827720": "sports_discussion",
        "24183782797": "sports_discussion",
        "25268330822": "book_discussion",
        "26295090920": "work_school",
        "26656170334": "work_school",
        "26672586157": "advertising_spam",
        "27351595027": "gaming",
        "27611416015": "advertising_spam",
        "27648269875": "work_school",
        "12846771407425536": "article_sharing",
        "12894521331286016": "sports_discussion",
    }
    apply_overrides(technology_rows, technology_overrides, "Technology review override: ")

    reaction_rows = load_csv(reaction_path)
    reaction_overrides = {
        "11329456268": "reaction",
        "11329472208": "reaction",
        "14022062393790464": "reaction",
        "19393414977": "criticism",
        "20454351424": "food_related",
        "21130664398": "article_sharing",
        "22432352128": "article_sharing",
        "22432430878": "article_sharing",
    }
    apply_overrides(reaction_rows, reaction_overrides, "Darwin audit: ")

    irony_updates = {
        "9690777251": ("true", "`#dafuq lmao` is explicitly joking disbelief."),
        "12366342472": ("true", "`hahaha ... dafuq` marks playful nonliteral reaction."),
        "14744924506": ("true", "`#dafuq ... lol` is joking exasperation."),
        "19618915098": ("true", "`#DaFuq lol` is overt humorous incredulity."),
        "22183722783": ("true", "`LOL ... DAFUQ` is comic disbelief."),
        "11248061288": ("true", "`LOL!` frames the workaround complaint playfully."),
        "12463495178": ("true", "Repeated joking markers and smiley make the tech row playful."),
        "11305554244800512": ("true", "`#ftw!! ... haha` is self-aware hype."),
        "19613374656552960": ("true", "`LOL` marks the workaround note as playful."),
    }
    apply_irony_updates(
        {"technology": technology_rows, "reaction": reaction_rows},
        irony_updates,
    )

    write_csv(technology_path, technology_rows)
    write_csv(reaction_path, reaction_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (technology_rows, reaction_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    print("technology_contexts", Counter(row["usage_context"] for row in technology_rows).most_common())
    print("technology_irony", Counter(row["is_ironic"] for row in technology_rows).most_common())
    print("reaction_irony", Counter(row["is_ironic"] for row in reaction_rows).most_common())


if __name__ == "__main__":
    main()
