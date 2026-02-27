from utils.colors import *
from utils.echo import *
from utils.cookie_parser import parse_cookie

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import requests
import csv
import os
import time

BASE_URL = "https://git.ir"


def execute():
    print(f"\n{MAGENTA}{BOLD}🚀 Course Scraper Started 🚀{RESET}\n")
    crawl()
    update_all_subtitles()


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def crawl():
    course_url = input(
        f"{CYAN}{BOLD}🩵 Paste course url: {RESET}"
    ).strip().rstrip("/")
    course_title = course_url.split("git.ir/")[-1]
    driver = create_driver()

    try:
        print(f"{YELLOW}🌐 Opening course page...{RESET}")
        driver.get(course_url)
        WebDriverWait(driver, 20)
        time.sleep(2)

        print(f"{BLUE}🔍 Collecting lectures...{RESET}")
        lectures = driver.execute_script(JS_SCRIPT)

        if not lectures:
            print(f"{RED}❌ No lectures found!{RESET}")
            return

        print(f"\n{GREEN}{BOLD}✨ {len(lectures)} Lectures Found ✨{RESET}\n")

        for i, item in enumerate(lectures, 1):
            print(
                f"{GREEN}{BOLD}[{i}]{RESET} "
                f"{CYAN}{item['section']}{RESET} "
                f"→ {WHITE}{item['title']}{RESET}"
            )

        file_path = save_lectures(course_title, lectures)
        print(f"\n{MAGENTA}💾 Saved to:{RESET} {YELLOW}{file_path}{RESET}")
        print(f"{GREEN}{BOLD}✅ Lectures Scraped Successfully!{RESET}\n")

    finally:
        driver.quit()


def save_lectures(course_title, lectures):
    os.makedirs("data/lectures", exist_ok=True)
    file_path = os.path.join(
        "data", "lectures", f"course-{course_title}.csv"
    )
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["section", "title", "dataItem", "dataIndex"],
        )
        writer.writeheader()
        writer.writerows(lectures)
    return file_path


def create_session(course_title):
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/144.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{BASE_URL}/{course_title}",
    })
    cookies = parse_cookie()
    for key, value in cookies.items():
        session.cookies.set(key, value)
    return session


def fetch_subtitle(session, lecture_id):
    url = f"{BASE_URL}/api/post/get-video/{lecture_id}"
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        return data["subtitles"][0]["src"] if data.get("subtitles") else ""
    except Exception:
        return ""


def get_subtitles_for_course(course_file):
    course_title = os.path.basename(course_file).replace("course-", "").replace(".csv", "")
    session = create_session(course_title)
    rows, fieldnames = read_csv(course_file)

    print(f"\n{BLUE}🎧 Fetching subtitles for {course_title}...{RESET}\n")

    for row in rows:
        lecture_id = row["dataItem"]
        row["subtitle"] = fetch_subtitle(session, lecture_id)
        print(
            f"{GREEN}{row['title']}{RESET} "
            f"→ {YELLOW}{row['subtitle']}{RESET}"
        )

    write_csv(course_file, rows, fieldnames)
    print(f"\n{MAGENTA}💾 Subtitles Updated:{RESET} {YELLOW}{course_file}{RESET}\n")


def read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        if "subtitle" not in fieldnames:
            fieldnames.append("subtitle")
        for row in reader:
            rows.append(row)
    return rows, fieldnames


def write_csv(path, rows, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_all_subtitles():
    lectures_dir = "data/lectures"
    if not os.path.isdir(lectures_dir):
        print(f"{RED}❌ No lectures folder found!{RESET}")
        return

    csv_files = [
        os.path.join(lectures_dir, f)
        for f in os.listdir(lectures_dir)
        if f.endswith(".csv")
    ]

    if not csv_files:
        print(f"{RED}❌ No lecture CSV files found!{RESET}")
        return

    for file in csv_files:
        get_subtitles_for_course(file)


JS_SCRIPT = """
const sections = document.querySelectorAll(".card.course-lectures");
const results = [];

sections.forEach(section => {
    const header = section.querySelector(".course-lecture-header h2");
    const sectionTitle = header ? header.innerText.trim() : "Untitled Section";

    const collapse = section.querySelector(".course-lecture-list");
    if (collapse && collapse.classList.contains("collapse")) {
        header.parentElement.click();
    }

    const items = section.querySelectorAll("a.video-playlist-item");

    items.forEach(item => {
        const titleEl = item.querySelector("h3");
        const title = titleEl ? titleEl.innerText.trim() : "";

        if (title) {
            results.push({
                section: sectionTitle,
                title: title,
                dataItem: item.getAttribute("data-item"),
                dataIndex: item.getAttribute("data-index")
            });
        }
    });
});

return results;
"""