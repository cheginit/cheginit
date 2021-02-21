
import sqlite_utils
from pathlib import Path
import re
import sys

tils_root = Path(sys.argv[1])
db = sqlite_utils.Database(tils_root.joinpath("tils.db"))

sql = "select path, title, url, topic, slug, created_utc from til order by created_utc desc limit 5"
tils = db.execute_returning_dicts(sql)

base = "https://github.com/cheginit/til/blob/main"
tils_md = "<br>".join(
    [
        f'[{t["title"]}]({base}/{t["topic"]}/{t["slug"]}.md) - {t["created_utc"].split("T")[0]}'
        for t in tils
    ]
)

r = re.compile(
    r"<!\-\- tils starts \-\->.*<!\-\- tils ends \-\->",
    re.DOTALL,
)

with open("README.md", "r") as readme:
    readme_contents = readme.read()

with open("README.md", "w") as readme:
    chunk = f"<!-- tils starts -->{tils_md}<!-- tils ends -->"
    readme.write(r.sub(chunk, readme_contents))

