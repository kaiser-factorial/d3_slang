import csv
from pathlib import Path

root = Path('/Users/corinakaiser/Desktop/Slang_InfoViz_FinalProj')
path = root / "2010_tweets_slang_filtering_working.csv"
keep_ids = ['10022511396', '10022523268', '10750813650', '11102358673', '11102359151', '11338464777', '12015247100', '12723822826356736', '14003902020', '14034349941', '14035751659', '16056030123261952', '16488525599', '19368268738', '2070665741991936', '22582151427', '23980766666', '23984978659', '24264396614', '24264571257', '26476620919', '29061001134', '7230166648492032', '7337456534', '7435475879', '7679790060', '7698032446', '8762796528', '8770086949', '9256261989', '9307597953830912']

with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fieldnames = list(rows[0].keys())
for row in rows:
    if row["usage_context"] == "advertising_spam":
        if row["id"] in keep_ids:
            row["keep_for_slang_analysis"] = "true"
            row["exclusion_reason"] = ""
        else:
            row["keep_for_slang_analysis"] = "false"
            row["exclusion_reason"] = "advertising_or_spam"
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
