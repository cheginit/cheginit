"""Update README.md by adding the five recent TILs."""
import re

import sqlite_utils


if __name__ == "__main__":
    db = sqlite_utils.Database("tils.db")

    sql = "select path, title, url, topic, slug, created_utc from til order by created_utc desc limit 10"
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

    with open("README.md") as readme:
        readme_contents = readme.read()

    with open("README.md", "w") as readme:
        chunk = f"<!-- tils starts -->{tils_md}<!-- tils ends -->"
        readme.write(r.sub(chunk, readme_contents))
