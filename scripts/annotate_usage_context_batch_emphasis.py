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


def classify_emphasis(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "bupkis":
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "excel", "it knowing", "facebook", "twitter", "macrumors", "ipad"):
            return out("technology_discussion")
        if contains(lowered, "work for bupkis", "living wage", "biz dev", "delivered bupkis", "means bupkis", "got bupkis"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "trying targeted crowd sourcing", "still not sure", "score big"):
            return out("self_description")
        return out("commenting")

    if word == "hells":
        if contains(lowered, "hells bells", "ac/dc", "#nowplaying", "now playing"):
            return out("music_discussion")
        if contains(lowered, "#news", "future - sacramaniacsmc", "disclosure nukes"):
            return out("article_sharing")
        if contains(lowered, "hells yes", "hells yeah", "oh hells no", "hells naw", "hells yah"):
            return out("reaction")
        if "@" in text:
            return out("casual_conversation")
        if contains(lowered, "cripple", "hungry as all hells", "i'm sad"):
            return out("self_description")
        return out("reaction")

    if word == "lowkey":
        if contains(lowered, "#nowplaying", "favorite songs", "fucks with chip tha rip"):
            return out("music_discussion")
        if contains(lowered, "lowkey bored", "lowkey scary", "i feel like", "i lowkey miss", "lowkey tired", "pissed me off", "hurt his feelings"):
            return out("self_description")
        if contains(lowered, "stop hatin", "you wish", "agreement", "actors", "barbie world"):
            return out("commenting")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("commenting")

    if word == "motherfucking":
        if contains(lowered, "snakes on this motherfucking plane", "holding back the motherfucking years", "lil wayne", "#nowplaying", "quote"):
            return out("music_discussion")
        if contains(lowered, "connection", "stay online", "site that reviews", "mw2", "lagged session", "internet"):
            return out("technology_discussion")
        if contains(lowered, "#wjc", "jordan eberle", "lost"):
            return out("sports_discussion")
        if contains(lowered, "good motherfucking morning", "motherfucking boo", "popeyes is the motherfucking best", "motherfucking useless", "mind yo own motherfucking business"):
            return out("reaction")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "late and snowing", "windchill of 3", "i hate", "seeing minka kelly"):
            return out("self_description")
        return out("commenting")

    if word == "relly":
        if contains(lowered, "@prettyrelly", "@relly_got_fetti", "@freaky_relly", "@rockstarrellrsg"):
            return out("casual_conversation")
        if contains(lowered, "relly looked gud", "did relly good", "feel relly sad", "got to stop dremming", "not relly,im vexed", "i relly wonder"):
            return out("self_description")
        if contains(lowered, "show called super manny", "secretturnon", "support d c", "shoutout"):
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
    emphasis_path = BATCH_DIR / "emphasis.csv"
    attraction_path = BATCH_DIR / "attraction.csv"

    emphasis_rows = load_csv(emphasis_path)
    for row in emphasis_rows:
        context, ironic, note = classify_emphasis(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    emphasis_overrides = {
        "7325704366": "commenting",
        "7367889187": "article_sharing",
        "7665160097": "article_sharing",
        "8281261846": "advertising_spam",
        "8288725783": "technology_discussion",
        "8304396237": "technology_discussion",
        "8826410766": "advertising_spam",
        "8827656446": "television_reference",
        "9857076072": "work_school",
        "12207443497": "casual_conversation",
        "12207676237": "casual_conversation",
        "12207741213": "casual_conversation",
        "12207800751": "casual_conversation",
        "12207888630": "casual_conversation",
        "12208016782": "casual_conversation",
        "12208242656": "casual_conversation",
        "12224162862": "article_sharing",
        "12230791326": "article_sharing",
        "13629002971": "casual_conversation",
        "13629244796": "casual_conversation",
        "13636798549": "humor",
        "13638242616": "humor",
        "13927084686": "casual_conversation",
        "14004546239": "advertising_spam",
        "14008977129": "advertising_spam",
        "14880183864": "article_sharing",
        "14939415230": "advertising_spam",
        "14939568096": "advertising_spam",
        "15053671083": "article_sharing",
        "15228172392": "casual_conversation",
        "15228363798": "casual_conversation",
        "15232089238": "casual_conversation",
        "15303963837": "article_sharing",
        "15317756346": "article_sharing",
        "15343468543": "advertising_spam",
        "16273835803": "advertising_spam",
        "16273881727": "casual_conversation",
        "16334718896": "sports_discussion",
        "16335391072": "advertising_spam",
        "18129807592": "casual_conversation",
        "18130265429": "casual_conversation",
        "20408819071": "casual_conversation",
        "20576114600": "article_sharing",
        "24784053027": "article_sharing",
        "27499593946": "television_reference",
        "27828351325": "sports_discussion",
        "27968523779": "advertising_spam",
        "711494777970689": "advertising_spam",
        "712638975709184": "advertising_spam",
        "712717916704768": "advertising_spam",
        "715664469790720": "advertising_spam",
        "721446535962624": "advertising_spam",
        "725970742935552": "advertising_spam",
        "732995661070336": "advertising_spam",
        "734312680914945": "advertising_spam",
        "7882131283906560": "article_sharing",
        "7886867349381120": "article_sharing",
        "7887463552917504": "article_sharing",
        "7892516128956416": "article_sharing",
        "8131645257293824": "article_sharing",
        "11643892319391744": "casual_conversation",
        "15506119711531008": "casual_conversation",
        "15506380995690496": "casual_conversation",
        "7303729030": "self_description",
        "7303739943": "reaction",
        "7303997574": "casual_conversation",
        "7476329666": "music_discussion",
        "7476419635": "article_sharing",
        "7476427306": "casual_conversation",
        "7476573302": "book_discussion",
        "8271032510": "advertising_spam",
        "8623846718": "advertising_spam",
        "8624051031": "fashion_beauty",
        "8624116309": "casual_conversation",
        "8717939060": "advertising_spam",
        "8718151339": "sports_discussion",
        "8994198677": "article_sharing",
        "8994421768": "sports_discussion",
        "9995905942": "work_school",
        "10063814062": "drug_context",
        "10063931489": "music_discussion",
        "10317425969": "music_discussion",
        "10334585147": "news_reaction",
        "10863157969": "fashion_beauty",
        "11926801854": "gaming",
        "13059394041": "gaming",
        "16913161909": "casual_conversation",
        "17047464485": "casual_conversation",
        "19503303943520256": "gaming",
        "19503509514752000": "music_discussion",
        "8441497781": "self_description",
        "8441518778": "casual_conversation",
        "8441561843": "self_description",
        "8441570428": "casual_conversation",
        "8441619995": "commenting",
        "8441717429": "self_description",
        "8441758328": "commenting",
        "8441807986": "storytelling",
        "8441948829": "commenting",
        "8442008189": "casual_conversation",
        "8442036361": "commenting",
        "8442054999": "self_description",
        "8442075851": "casual_conversation",
        "8442195863": "criticism",
        "8442216033": "reaction",
        "8442221595": "self_description",
        "11461557057": "music_discussion",
        "15288534030": "casual_conversation",
        "27671192087": "self_description",
        "7428333681": "commenting",
        "7428344082": "sports_discussion",
        "7428449079": "food_related",
        "7428713117": "article_sharing",
        "7428788048": "music_discussion",
        "7429177565": "reaction",
        "7429362421": "humor",
        "7429413647": "gaming",
        "7429725587": "reaction",
        "7516809591": "article_sharing",
        "7517869013": "technology_discussion",
        "7517170938": "self_description",
        "7517281156": "commenting",
        "7517311351": "food_related",
        "7600932080": "celebrity_gossip",
        "12092780084": "television_reference",
        "15187557126": "casual_conversation",
        "17767563683": "technology_discussion",
        "18914921609": "reaction",
        "21615798322": "article_sharing",
        "25763110894": "gaming",
        "5475578480168960": "music_discussion",
        "8293109018": "self_description",
        "8293235470": "casual_conversation",
        "8294343093": "casual_conversation",
        "8294460927": "self_description",
        "8294771680": "television_reference",
        "8294953846": "self_description",
        "8295055063": "casual_conversation",
        "8295540408": "compliment",
        "8295617402": "casual_conversation",
        "8295829218": "casual_conversation",
        "9066247191": "news_reaction",
        "9066523818": "self_description",
        "9066275272": "casual_conversation",
        "9066286331": "casual_conversation",
        "9066290088": "casual_conversation",
        "9107606268": "casual_conversation",
        "12336006480": "compliment",
        "17228307580": "casual_conversation",
        "23078051320": "casual_conversation",
        "4071003323891712": "commenting",
    }
    apply_overrides(emphasis_rows, emphasis_overrides, "Manual override -> ")

    attraction_rows = load_csv(attraction_path)
    attraction_overrides = {
        "8276688599": "article_sharing",
        "8592307875": "celebrity_gossip",
        "7326108899": "compliment",
        "7311081036": "casual_conversation",
        "7315299564": "humor",
        "7315340064": "casual_conversation",
        "7315356018": "casual_conversation",
        "8601495697": "casual_conversation",
        "8783442059": "criticism",
        "13623853021": "music_discussion",
        "9409159594254336": "music_discussion",
    }
    apply_overrides(attraction_rows, attraction_overrides, "Darwin audit -> ")

    irony_updates = {}
    irony_updates = {
        "22438304058": ("true", "Contains 'just kidding', explicitly marking the hells line as joking."),
        "15288712686": ("true", "Contains 'lol jk but lowkey serious', so the line is at least partly playful/ironic."),
        "20094209688084480": ("true", "Contains 'lol jk', explicitly canceling the baby-daddy line."),
        "9108891042": ("true", "Contains 'Just kiddinggggggg!!!! Lol', making the relly claim nonliteral."),
    }
    apply_irony_updates(
        {
            "emphasis": emphasis_rows,
            "attraction": attraction_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, emphasis_rows)
    sync_batch_to_master(master_rows, attraction_rows)

    write_csv(emphasis_path, emphasis_rows)
    write_csv(attraction_path, attraction_rows)
    write_csv(MASTER_PATH, master_rows)

    print("emphasis usage_context counts:", Counter(row["usage_context"] for row in emphasis_rows))
    print("emphasis is_ironic counts:", Counter(row["is_ironic"] for row in emphasis_rows))
    print("attraction is_ironic counts:", Counter(row["is_ironic"] for row in attraction_rows))


if __name__ == "__main__":
    main()
