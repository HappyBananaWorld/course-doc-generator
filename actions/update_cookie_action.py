from utils.colors import *
from utils.echo import echo
import os
import csv

def execute():
    cookie = input(f"{YELLOW}🍪 Enter New Cookie: {RESET}",)

    file_path = os.path.join("data", "config.csv")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    rows = []

    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))

    updated = False
    for row in rows:
        if row["key"] == "cookie":
            row["value"] = cookie
            updated = True
            break

    if not updated:
        rows.append({"key": "cookie", "value": cookie})

    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["key", "value"])
        writer.writeheader()
        writer.writerows(rows)

    echo(f"{GREEN}✅ Cookie saved successfully!{RESET}")
