import csv
import requests
import os

# ---------- مسیر فایل CSV ----------
course_title = "pluralsight-clean-architecture-patterns-practices-and-principles"
csv_file = os.path.join("lectures", f"course-{course_title}.csv")

# ---------- ایجاد سشن ----------
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"https://git.ir/{course_title}"
})

session.cookies.set("user_source", "aHR0cHM6Ly9naXQuaXIv")
session.cookies.set("csrftoken", "5H8jjqFdgjJyWeYR9vfVjLK9IS58AEdCQ6C4asUEbHs8rTXZdCCzxteFmCaeSLuH")
session.cookies.set("sessionid", "z2cajtm17epnqivftv0cilztryb5x3hg")

# ---------- خواندن CSV ----------
rows = []
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    if "subtitle" not in fieldnames:
        fieldnames.append("subtitle")  # اضافه کردن ستون subtitle
    for row in reader:
        rows.append(row)

# ---------- بروزرسانی subtitle ----------
for row in rows:
    lecture_id = row['dataItem']
    url = f"https://git.ir/api/post/get-video/{lecture_id}"

    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        subtitle_link = data['subtitles'][0]['src'] if data.get('subtitles') else ""
    except Exception as e:
        print(f"Error fetching lecture {lecture_id}: {e}")
        subtitle_link = ""

    row['subtitle'] = subtitle_link
    print(f"{row['title']} -> subtitle: {subtitle_link}")

# ---------- نوشتن دوباره CSV همان فایل ----------
with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV updated: {csv_file}")