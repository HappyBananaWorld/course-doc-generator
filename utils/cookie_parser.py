from .colors import *
from .echo import echo
import os
import csv


def get_cookie():
    file_path = os.path.join('data', "config.csv")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return next((row["value"] for row in reader if row["key"] == "cookie"), None)


def parse_cookie():
    try:
        cookie = get_cookie()

        split = cookie.split(';')

        return {
            "user_source": split[0].split("=")[1].strip(),
            "csrftoken": split[1].split("=")[1].strip(),
            "sessionid": split[2].split("=")[1].strip(),
        }
    except:
        echo(f"{RED}⚠️ Invalid cookie format pls update your cookie!{RESET}")