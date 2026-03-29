import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / "2010_tweets_slang_filtering_working.csv"
keep_ids = ['10054211635', '10055519179', '10114883009', '10447051374', '10660996439', '10750811993', '11302393185', '11842350005', '11842378557', '11842449528', '11842468197', '12857555382', '13035588804', '13035622188', '14003902020', '16073214964', '16073356619', '16376694899', '16376738763', '16376770165', '17156500350', '17158096540', '19368268738', '29523234004', '29523279281', '29523326755', '29523360617', '7337456534', '7401267442', '7432591106', '7666200995', '7679790060', '7698032446', '7764889768', '7826244224', '7834104250', '7868880364', '7923370511', '8080190809', '8166736353', '8224609560', '8344714868', '8361273933', '8364756325', '8380777555', '8425148356', '8425186905', '8485634164', '8623629138', '8684606173', '8685869412', '8697746010', '8719023235', '8719309997', '9418642056', '9500164080', '9508335189', '9508768695', '9768960778', '9948776187', '9948909175']

with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fieldnames = list(rows[0].keys())
for row in rows:
    if row["usage_context"] == "article_sharing":
        if row["id"] in keep_ids:
            row["keep_for_slang_analysis"] = "true"
            row["exclusion_reason"] = ""
        else:
            row["keep_for_slang_analysis"] = "false"
            txt = (row["text"] or "").lower()
            if any(x in txt for x in ["http", "bit.ly", "tinyurl", "fb.me", "twitpic"]) and (":" in txt or "rt @" in txt or "via @" in txt):
                row["exclusion_reason"] = "title_or_media_reference"
            else:
                row["exclusion_reason"] = "meta_word_reference"
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
