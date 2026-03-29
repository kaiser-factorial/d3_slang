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


def classify_humor(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"

    def out(ctx: str, note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, note

    if word == "roshambo":
        if contains(lowered, "roshambo winery", "glass of roshambo") or ("http" in lowered and contains(lowered, "roshambo")):
            return out("article_sharing")
        if contains(lowered, "the network - roshambo", "money money 2020"):
            return out("music_discussion")
        if contains(lowered, "spike.com", "search roshambo", "mean girls", "pootie tang"):
            return out("television_reference")
        if contains(lowered, "roshambo me", "roshambo for it", "#roshambo the mailman", "roshambo'd with my wingman", "i go first"):
            return out("humor")
        if "@" in text:
            return out("casual_conversation")
        return out("commenting")

    if word == "shart":
        if contains(lowered, "shart myself", "shart yaself", "shart in ur mouth", "googling pictures of sharks", "huge mistake", "#dateisover", "lookinass", "blowout", "what do shart mean"):
            return out("humor")
        if contains(lowered, "beans at moes", "just don't shart on me", "did he shart", "@bgever shart"):
            return out("casual_conversation")
        if "@" in text:
            return out("casual_conversation")
        if "http" in lowered:
            return out("article_sharing")
        return out("humor")

    if word == "shtick":
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "wimbledon", "youth in revolt", "samberg", "gov. patterson", "marvel movie", "turner d. century", "conan"):
            return out("television_reference")
        if contains(lowered, "bio shtick", "touring shtick", "same old shtick", "his shtick", "my 'shtick'", "awkward he can truly be", "ginobiliiiiiii shtick"):
            return out("commenting")
        if contains(lowered, "quality shtick for my office", "cute shtick", "great laughs"):
            return out("humor")
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
    humor_path = BATCH_DIR / "humor.csv"
    sex_path = BATCH_DIR / "sex.csv"

    humor_rows = load_csv(humor_path)
    for row in humor_rows:
        context, ironic, note = classify_humor(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    humor_overrides = {
        "7350670399": "casual_conversation",
        "7353054077": "humor",
        "7380583554": "food_related",
        "7380624078": "casual_conversation",
        "7672872617": "sports_discussion",
        "7685616556": "casual_conversation",
        "7686088761": "article_sharing",
        "7686385816": "technology_discussion",
        "7687269578": "humor",
        "7691146663": "humor",
        "7694551856": "music_discussion",
        "7840049786": "casual_conversation",
        "7842061546": "casual_conversation",
        "8078480420": "article_sharing",
        "8078517506": "article_sharing",
        "8078693621": "article_sharing",
        "8078896019": "article_sharing",
        "8078914768": "article_sharing",
        "8081615025": "article_sharing",
        "8083178113": "article_sharing",
        "8085311918": "article_sharing",
        "8089544013": "food_related",
        "8117368263": "article_sharing",
        "8132468811": "sports_discussion",
        "8151969920": "food_related",
        "8163166040": "article_sharing",
        "8164825744": "sports_discussion",
        "8164847425": "sports_discussion",
        "8428431760": "casual_conversation",
        "8430269602": "casual_conversation",
        "8505642179": "gaming",
        "8546115151": "meme_reference",
        "8553184767": "advertising_spam",
        "8562531383": "advertising_spam",
        "8568269503": "technology_discussion",
        "8685842143": "advertising_spam",
        "8696661071": "advertising_spam",
        "9308914821": "music_discussion",
        "9315818094": "music_discussion",
        "9316781438": "casual_conversation",
        "10101560965": "humor",
        "10101728314": "article_sharing",
        "10104339859": "humor",
        "10105872371": "gaming",
        "10121397302": "sports_discussion",
        "10127886129": "advertising_spam",
        "10127922780": "advertising_spam",
        "10243890064": "casual_conversation",
        "10253160245": "music_discussion",
        "10686379103": "food_related",
        "10686437641": "food_related",
        "10698132315": "casual_conversation",
        "10710271039": "casual_conversation",
        "10724189204": "sports_discussion",
        "10724883414": "sports_discussion",
        "11292811476": "technology_discussion",
        "11326979841": "music_discussion",
        "11346150721": "article_sharing",
        "11502826929": "technology_discussion",
        "11503248918": "technology_discussion",
        "11510390646": "music_discussion",
        "11510518549": "advertising_spam",
        "11516690025": "casual_conversation",
        "11522979808": "casual_conversation",
        "11525287417": "gaming",
        "11787486334": "advertising_spam",
        "12496166836": "music_discussion",
        "12723172452": "food_related",
        "12736212985": "advertising_spam",
        "12752270889": "music_discussion",
        "12775204626": "music_discussion",
        "13049812409": "advertising_spam",
        "13053035231": "fashion_beauty",
        "13297319432": "casual_conversation",
        "13303794701": "music_discussion",
        "13303817894": "music_discussion",
        "13312520208": "article_sharing",
        "13314502692": "advertising_spam",
        "13319422840": "article_sharing",
        "13325902218": "article_sharing",
        "13415547496570880": "article_sharing",
        "20117317505515520": "article_sharing",
        "21005594286620672": "casual_conversation",
        "14277561829": "humor",
        "25619346299": "casual_conversation",
        "7805224354": "humor",
        "7805466994": "humor",
        "7806037448": "casual_conversation",
        "7807909954": "commenting",
        "7809559770": "technology_discussion",
        "7811965726": "humor",
        "7812191898": "casual_conversation",
        "7812213374": "commenting",
        "7812229511": "humor",
        "7812542334": "humor",
        "8565374995": "humor",
        "8566510961": "casual_conversation",
        "8567288863": "casual_conversation",
        "8571120988": "casual_conversation",
        "8573109167": "dating_context",
        "8574977325": "humor",
        "8580451442": "television_reference",
        "8586023775": "music_discussion",
        "9290074065": "casual_conversation",
        "9295387895": "meme_reference",
        "9297154128": "meme_reference",
        "9299689143": "meme_reference",
        "9299722882": "meme_reference",
        "9302403071": "music_discussion",
        "9303093632": "casual_conversation",
        "9531483419": "commenting",
        "9531525800": "casual_conversation",
        "10406155201": "sports_discussion",
        "10410264043": "work_school",
        "10412606696": "casual_conversation",
        "10412658251": "casual_conversation",
        "12076043178": "television_reference",
        "12076527448": "self_description",
        "12076673706": "reaction",
        "12085271446": "storytelling",
        "12747247613": "casual_conversation",
        "12757287319": "casual_conversation",
        "12757328507": "casual_conversation",
        "12766509373": "article_sharing",
        "14352245385": "self_description",
        "14353954017": "article_sharing",
        "14361294012": "casual_conversation",
        "17599270720": "casual_conversation",
        "17607270617": "technology_discussion",
        "17618178479": "reaction",
        "10255832087": "casual_conversation",
        "17782415666": "casual_conversation",
        "23909558867": "humor",
        "19539061156876288": "humor",
        "7484001820": "casual_conversation",
        "7485238588": "technology_discussion",
        "7485449165": "article_sharing",
        "7485449505": "article_sharing",
        "7487324084": "television_reference",
        "7488386342": "humor",
        "7489021602": "commenting",
        "7490802817": "article_sharing",
        "7494139303": "casual_conversation",
        "7583165222": "article_sharing",
        "7583180064": "self_description",
        "7583599129": "commenting",
        "7584530176": "television_reference",
        "7596210459": "casual_conversation",
        "7596249181": "casual_conversation",
        "7601840928": "celebrity_gossip",
        "7602915869": "article_sharing",
        "8058200832": "celebrity_gossip",
        "8058448230": "television_reference",
        "8058591685": "celebrity_gossip",
        "8059050641": "self_description",
        "8060897551": "music_discussion",
        "8061916606": "celebrity_gossip",
        "8090663500": "music_discussion",
        "8096221408": "criticism",
        "10266422238": "commenting",
        "13041440857": "humor",
        "15563402828": "television_reference",
        "19388685053": "commenting",
        "24689203548": "commenting",
        "1247363872071680": "self_description",
        "15656329217572864": "sports_discussion",
    }
    apply_overrides(humor_rows, humor_overrides, "Manual override -> ")

    sex_rows = load_csv(sex_path)
    sex_overrides = {
        "7665617485": "self_description",
        "8281261846": "article_sharing",
        "8442242273": "television_reference",
        "15289356275": "television_reference",
        "19688324466": "television_reference",
        "7518093615": "reaction",
        "7518303992": "criticism",
        "10334434392": "music_discussion",
        "11939661392": "television_reference",
        "12320363968": "television_reference",
        "12010395679": "television_reference",
        "27061049943": "television_reference",
        "27073608087": "television_reference",
        "7671365675": "advertising_spam",
        "8640220605": "fashion_beauty",
    }
    apply_overrides(sex_rows, sex_overrides, "Darwin audit -> ")

    irony_updates = {
        "29547380158": ("true", "Contains 'hahaha jk', explicitly marking the shart threat as joking."),
        "8705487948218370": ("true", "Contains 'Just kidding', making the shtick line overtly playful."),
        "21000583111": ("true", "Contains teasing 'haha' plus wink around 'get rapey', so it reads as nonliteral."),
    }
    apply_irony_updates(
        {
            "humor": humor_rows,
            "sex": sex_rows,
        },
        irony_updates,
    )

    master_rows = load_csv(MASTER_PATH)
    sync_batch_to_master(master_rows, humor_rows)
    sync_batch_to_master(master_rows, sex_rows)

    write_csv(humor_path, humor_rows)
    write_csv(sex_path, sex_rows)
    write_csv(MASTER_PATH, master_rows)

    print("humor usage_context counts:", Counter(row["usage_context"] for row in humor_rows))
    print("humor is_ironic counts:", Counter(row["is_ironic"] for row in humor_rows))
    print("sex is_ironic counts:", Counter(row["is_ironic"] for row in sex_rows))


if __name__ == "__main__":
    main()
