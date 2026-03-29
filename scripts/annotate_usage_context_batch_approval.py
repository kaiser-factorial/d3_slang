from __future__ import annotations

import csv
import re
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


def classify_approval(row: dict[str, str]) -> tuple[str, str, str]:
    text = row["text"]
    lowered = text.lower()
    word = row["word"]
    ironic = "false"
    note = ""

    def out(ctx: str, local_note: str = "") -> tuple[str, str, str]:
        return ctx, ironic, local_note

    if word == "DFTBA":
        if contains(
            lowered,
            "preorder",
            "pre-order",
            "release date",
            "shipping",
            "ships today",
            "shop/products",
            "pizza-john",
            "bracelet",
            "bracelets",
            "$7 each",
            "paypal",
            "pre-ordered",
            "available for pre-order",
        ) or "dftba.com/shop" in lowered:
            return out("advertising_spam", "DFTBA merch/brand promotion.")
        if contains(
            lowered,
            "itunes",
            "album",
            "cd",
            "track",
            "tracks",
            "artists",
            "music",
            "song",
            "songs",
            "youtube",
            "lullab",
            "tunevibez",
            "#musicmonday",
            "dftbarecords",
            "karaoke",
        ):
            return out("music_discussion", "DFTBA used as label/slogan in music context.")
        if contains(lowered, "blogstyle", "new blog", "question monday") or (
            "http" in lowered
            and not contains(
                lowered,
                "youtube",
                "itunes",
                "album",
                "cd",
                "track",
                "music",
                "song",
                "dftba.com",
            )
        ):
            return out("article_sharing", "DFTBA slogan attached to link sharing.")
        if contains(lowered, "awesome person", "congratulations", "best wishes"):
            return out("compliment")
        if "@" in text or contains(
            lowered,
            "good morning",
            "time for bed",
            "see you later",
            "hi ",
            "hope ",
            "thanks",
            "thank you",
            "at school",
            "math help",
            "you can do it",
            "staying sane",
        ):
            return out("casual_conversation")
        return out("commenting")

    if word == "bomb":
        if contains(lowered, "#epicpetwars", "giant bomb", "pipe bomb", "boomers"):
            return out("gaming", "Literal/game-title use of bomb.")
        if contains(
            lowered,
            "song",
            "album",
            "#nowplaying",
            "spotify",
            "itunes",
            "track",
            "music",
            "fluke",
            "n.e.r.d",
            "bomb first",
            "bomb the bass",
            "bomb the panhandle",
            "cherry bomb",
            "atomic bomb",
        ):
            return out("music_discussion", "Bomb appears in a song/artist/title context.")
        if contains(lowered, "n bomb", "drop the n bomb"):
            return out("criticism", "Refers to slur usage rather than approval slang.")
        if "http" in lowered and contains(
            lowered,
            "bomb threat",
            "car bomb",
            "bomb scare",
            "bomb plot",
            "package bomb",
            "bomb attack",
            "bomb explodes",
            "bomb explosion",
            "bomb injures",
            "warplanes bomb",
            "suicide bomb",
            "cluster bomb",
            "bombing",
            "bomb disposal",
            "bomb-sniffing",
            "bomb squad",
            "shoe bomb",
            "time bomb",
            "bomb prisons",
            "bomb suspect",
            "bomb test",
            "airport bomb",
            "moscow bomb",
            "explosive",
            "terrorist",
        ):
            return out("article_sharing", "Literal bomb/news link share.")
        if contains(
            lowered,
            "bomb threat",
            "car bomb",
            "bomb scare",
            "suicide bomb",
            "bomb plot",
            "warplanes bomb",
            "bombing",
            "terrorist",
            "nuclear",
        ):
            return out("news_reaction", "Literal bomb/news event reference.")
        if contains(
            lowered,
            "eatin",
            "tacos",
            "in and out",
            "corn flakes",
            "peach cobbler",
            "boston market",
            "johnny rockets",
            "grilled cheese",
        ):
            return out("food_related")
        if contains(lowered, "volunteer bomb", "bath bomb", "products.html"):
            return out("advertising_spam")
        if contains(lowered, "i'm the bomb", "im the bomb", "feel so bomb", "carrying a txt bomb", "costs a bomb"):
            if contains(lowered, "txt bomb", "costs a bomb", "feel so bomb"):
                return out("self_description", "Personal state/metaphor, not approval slang.")
            return out("humor" if contains(lowered, "tick-tick boom", "lol", "xd") else "commenting")
        if contains(lowered, "the bomb", "bomb-diggity", "bomb.net", "bomb ass"):
            if contains(lowered, "@") and contains(lowered, "you", "she", "he", "my people"):
                return out("compliment")
            return out("commenting")
        if contains(lowered, "joke", "haha", "lmao", "lmfao", "xd"):
            return out("humor")
        return out("commenting")

    if word == "fire":
        if contains(
            lowered,
            "#nowplaying",
            "song",
            "songs",
            "album",
            "cover",
            "video",
            "freestyle",
            "2ne1",
            "heaven's on fire",
            "floor on fire",
            "fire bomb",
            "rihanna",
            "fire state radio",
        ):
            return out("music_discussion", "Fire appears in song/title/music context.")
        if contains(lowered, "rock band", "mario", "buttons to mash", "pipe to"):
            return out("gaming")
        if "http" in lowered and contains(
            lowered,
            "fire alarm",
            "caught fire",
            "fatal fire",
            "pub damaged in fire",
            "under fire",
            "draws fire",
            "crashed",
            "fire service",
            "animalshelter",
            "dangerous things",
            "fire releases",
            "fire & knives",
            "played with fire",
            "goldman",
            "girl who played with fire",
            "who played with fire",
            "fire brand",
        ):
            return out("article_sharing", "Literal/title use of fire in linked content.")
        if contains(lowered, "fatal fire", "caught fire", "under fire", "draws fire"):
            return out("news_reaction", "Literal/news use of fire.")
        if contains(
            lowered,
            "throat is on fire",
            "heart fire",
            "fire alarm has gone off",
            "fire alarm at",
            "fire yu on ur first day",
            "can't fire me",
            "cant fire me",
        ):
            if contains(lowered, "can't fire me", "cant fire me", "pants on fire"):
                return out("humor")
            return out("self_description")
        if contains(lowered, "this fire between us", "love is friendship set on fire"):
            return out("dating_context")
        if contains(lowered, "sure-fire ways", "adobe flash under fire"):
            return out("technology_discussion", "Tech/media phrase using fire non-slang.")
        if re.search(r"\bfire\b", lowered) and contains(lowered, " is fire", " fire!!!", "so fire", "fire!"):
            return out("compliment")
        return out("commenting")

    if word == "kosher":
        if "http" in lowered:
            return out("article_sharing", "Link share using literal kosher/religious/food sense.")
        if contains(lowered, "rabbi", "jew", "jewish", "god", "passover", "religious", "teamjesus", "chabad"):
            return out("religion")
        if contains(lowered, "restaurant", "salt", "milk", "meat", "wine", "cheese", "traveler", "food"):
            return out("food_related")
        if contains(lowered, "not kosher", "isn't kosher", "aint kosher"):
            return out("criticism")
        if contains(lowered, "he is kosher", "happy and kosher"):
            return out("compliment")
        return out("commenting", "General propriety/acceptability use of kosher.")

    if word == "next-level":
        if contains(lowered, "blunt", "toke"):
            return out("drug_context")
        if contains(lowered, "mario", "buttons to mash", "pipe to", "game", "mindflex"):
            return out("gaming")
        if contains(lowered, "ufc", "john wall", "#chargers", "fighting to join"):
            return out("sports_discussion")
        if contains(lowered, "scarf", "harajuku", "swagger backpack", "phenomenon pants"):
            return out("fashion_beauty")
        if contains(lowered, "keyword research", "business", "marketing", "income") and "http" in lowered:
            return out("advertising_spam")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "congrats", "congratulation", "thankyou for ur encouragement", "you follow to reach", "take your man to the next level"):
            return out("compliment")
        if contains(lowered, "i think i am officially", "gettin into a lift", "i feel we still"):
            return out("self_description")
        return out("commenting")

    if word == "rad":
        if contains(lowered, "gerhard von rad", "world christian books"):
            return out("book_discussion", "Proper-name/book listing use of Rad.")
        if contains(lowered, "rad fan", "radiator", "cvs, wag or rad", "rad kent"):
            return out("technology_discussion", "Non-slang technical/proper-noun use of rad.")
        if contains(lowered, "song", "show", "coachella", "band", "listen to this", "music", "dollhouse", "bar was fun", "shooting for @julietsband"):
            return out("music_discussion")
        if contains(lowered, "#chargers", "#nfl"):
            return out("sports_discussion")
        if "http" in lowered and contains(lowered, "twitpic", "photo:", "new logo", "store", "tumblr", "blog post"):
            return out("article_sharing")
        if contains(lowered, "date this weekend"):
            return out("dating_context")
        if contains(
            lowered,
            "picture is so rad",
            "fucking rad",
            "totally rad",
            "very rad",
            "pretty rad",
            "it's rad",
            "its rad",
            "rad people",
            "rad party",
            "rad night",
            "rad new store",
        ):
            return out("compliment")
        if "@" in text:
            return out("casual_conversation", "Handle/reply context with rad token.")
        return out("commenting")

    if word == "shiznat":
        if contains(lowered, "#3oh3tour", "steely dan", "studio together", "friday night music"):
            return out("music_discussion")
        if contains(lowered, "dexter", "farscape", "#supernatural"):
            return out("television_reference")
        if contains(lowered, "del taco", "johnny rockets", "sour apple", "grilled cheese"):
            return out("food_related")
        if contains(lowered, "holy shiznat", "oh shiznat"):
            return out("reaction")
        if "http" in lowered:
            return out("article_sharing")
        if contains(lowered, "is the shiznat"):
            return out("compliment")
        if contains(lowered, "my shiznat", "pick up my shiznat", "skype shiznat", "twitter shiznat", "work on my", "before the a.m.", "project"):
            return out("casual_conversation")
        if contains(lowered, "funny", "haha", "lol"):
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
    approval_path = BATCH_DIR / "approval.csv"
    food_path = BATCH_DIR / "food.csv"
    meme_path = BATCH_DIR / "meme.csv"
    animals_path = BATCH_DIR / "animals.csv"
    emotion_path = BATCH_DIR / "emotion.csv"
    religion_path = BATCH_DIR / "religion.csv"

    approval_rows = load_csv(approval_path)
    for row in approval_rows:
        context, ironic, note = classify_approval(row)
        row["usage_context"] = context
        row["is_ironic"] = ironic
        row["annotation_notes"] = note

    approval_overrides = {
        "7849377311": "humor",
        "7849392965": "food_related",
        "7849395731": "food_related",
        "7849395812": "music_discussion",
        "7849425816": "advertising_spam",
        "7946311663": "article_sharing",
        "7946325997": "article_sharing",
        "7946344710": "gaming",
        "7946351387": "music_discussion",
        "7946385096": "compliment",
        "8005507738": "music_discussion",
        "8005522065": "article_sharing",
        "8005561762": "self_description",
        "8005570221": "compliment",
        "8005573743": "self_description",
        "8005578224": "article_sharing",
        "8005578348": "food_related",
        "9726793221": "commenting",
        "9726834133": "article_sharing",
        "9726836914": "article_sharing",
        "9726852601": "news_reaction",
        "10799822487": "music_discussion",
        "11447182611": "article_sharing",
        "11447193865": "article_sharing",
        "11490013018": "humor",
        "11490014982": "article_sharing",
        "11490015000": "article_sharing",
        "11490015079": "music_discussion",
        "11490019254": "music_discussion",
        "11843015821": "article_sharing",
        "11843033491": "article_sharing",
        "11843056719": "article_sharing",
        "11843062435": "article_sharing",
        "11843062919": "article_sharing",
        "15818502820": "music_discussion",
        "15818504982": "music_discussion",
        "15818529310": "music_discussion",
        "15818552195": "article_sharing",
        "15818566979": "news_reaction",
        "16258359944": "news_reaction",
        "16258365494": "article_sharing",
        "16258383614": "news_reaction",
        "16258384615": "humor",
        "16258389491": "article_sharing",
        "18059765950": "compliment",
        "18059769162": "article_sharing",
        "18059802419": "article_sharing",
        "18690087115": "article_sharing",
        "18690097216": "article_sharing",
        "18690162501": "food_related",
        "18690189531": "article_sharing",
        "19355533748211712": "article_sharing",
        "19355739642400768": "article_sharing",
        "19355813822857216": "article_sharing",
        "19355869720354816": "news_reaction",
        "19355872178212864": "article_sharing",
        "19355941782691840": "article_sharing",
        "19549094789": "news_reaction",
        "19549099839": "article_sharing",
        "19549108444": "music_discussion",
        "19549120267": "humor",
        "20188966300": "humor",
        "21130657053": "commenting",
        "21130664453": "music_discussion",
        "21130676809": "compliment",
        "22432314853": "article_sharing",
        "22432320532": "commenting",
        "22690904292": "gaming",
        "22732809754": "article_sharing",
        "22732810838": "article_sharing",
        "22732812424": "article_sharing",
        "22732813723": "gaming",
        "22732820481": "article_sharing",
        "22732823645": "article_sharing",
        "22961174577": "advertising_spam",
        "22961183008": "criticism",
        "22961187125": "article_sharing",
        "23260875200": "article_sharing",
        "25888343894": "article_sharing",
        "25888405403": "article_sharing",
        "25888496742": "casual_conversation",
        "26730093635": "article_sharing",
        "26730118600": "article_sharing",
        "26730128116": "commenting",
        "26730151246": "article_sharing",
        "26730153309": "article_sharing",
        "26730179094": "article_sharing",
        "27161121696": "article_sharing",
        "27161158513": "article_sharing",
        "27161180776": "technology_discussion",
        "27871844231": "article_sharing",
        "27871845287": "advertising_spam",
        "27871847582": "article_sharing",
        "27871867689": "gaming",
        "28376221000": "reaction",
        "28376238279": "criticism",
        "28684289910": "music_discussion",
        "28684361756": "article_sharing",
        "28684389433": "technology_discussion",
        "28684405709": "article_sharing",
        "28684499816": "humor",
        "5317462371336192": "article_sharing",
        "5317605564874752": "article_sharing",
        "5317735349223424": "humor",
        "15526315239153664": "music_discussion",
        "21292221433118720": "article_sharing",
        "21292268946202624": "humor",
        "21292289099833344": "article_sharing",
        "21292300491554816": "music_discussion",
        "7316524855": "casual_conversation",
        "7331300636": "commenting",
        "7429111667": "compliment",
        "7896030683": "casual_conversation",
        "8206585166": "commenting",
        "9609651662": "advertising_spam",
        "10168620839": "casual_conversation",
        "10875777799": "commenting",
        "12066486656": "advertising_spam",
    }
    apply_overrides(approval_rows, approval_overrides, "Approval review override: ")

    food_rows = load_csv(food_path)
    food_overrides = {
        "7705033424": "advertising_spam",
        "7911632298": "advertising_spam",
        "9565979360": "advertising_spam",
        "13301207597": "advertising_spam",
        "15508299549": "article_sharing",
        "20335164568": "article_sharing",
        "20665409268": "article_sharing",
        "20665410819": "article_sharing",
        "20665411353": "article_sharing",
        "20666913847": "article_sharing",
    }
    apply_overrides(food_rows, food_overrides, "Darwin audit: ")

    meme_rows = load_csv(meme_path)
    animals_rows = load_csv(animals_path)
    emotion_rows = load_csv(emotion_path)
    religion_rows = load_csv(religion_path)

    irony_updates = {
        "20188966300": ("true", "Playful/nonliteral self-aware *DFTBA* phrasing."),
        "10444740757": ("true", "Overt comic/hyperbolic 'Warning Shots Fire! ... Lmfao!!!'."),
        "8005570221": ("true", "Playful exaggerated praise with 'the BOMB ... lol'."),
        "12573605542": ("false", "Casual chat with a person named Meme; not clear irony."),
        "6962169451126785": ("false", "Handle/name banter, not clear sarcasm."),
        "6963284351651841": ("false", "Ordinary conversational use with Meme as a name/handle."),
        "7674678735": ("true", "Clear playful hyperbole about mozzie vs skeeter."),
        "8203146401": ("true", "Comic exaggeration about mozzie sounding like a motorbike."),
        "7642477697": ("true", "Explicit comic exaggeration: 'actual conniption fit! LOL'."),
        "13140745541": ("true", "Overt self-canceling irony: 'JK God don't take me seriously'."),
    }
    apply_irony_updates(
        {
            "approval": approval_rows,
            "food": food_rows,
            "meme": meme_rows,
            "animals": animals_rows,
            "emotion": emotion_rows,
            "religion": religion_rows,
        },
        irony_updates,
    )

    write_csv(approval_path, approval_rows)
    write_csv(food_path, food_rows)
    write_csv(meme_path, meme_rows)
    write_csv(animals_path, animals_rows)
    write_csv(emotion_path, emotion_rows)
    write_csv(religion_path, religion_rows)

    master_rows = load_csv(MASTER_PATH)
    for batch_rows in (approval_rows, food_rows, meme_rows, animals_rows, emotion_rows, religion_rows):
        sync_batch_to_master(master_rows, batch_rows)
    write_csv(MASTER_PATH, master_rows)

    approval_contexts = Counter(row["usage_context"] for row in approval_rows)
    approval_irony = Counter(row["is_ironic"] for row in approval_rows)
    print("approval_contexts", approval_contexts.most_common())
    print("approval_irony", approval_irony.most_common())
    print("food_contexts", Counter(row["usage_context"] for row in food_rows).most_common())
    print("food_irony", Counter(row["is_ironic"] for row in food_rows).most_common())


if __name__ == "__main__":
    main()
