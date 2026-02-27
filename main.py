from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os
import json
import time

# ---------- تنظیمات مرورگر ----------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

course = "https://git.ir/pluralsight-clean-architecture-patterns-practices-and-principles"
course_title = course.split("git.ir/")[1]
driver.get(course)



wait = WebDriverWait(driver, 20)

# صبر کوتاه برای لود اولیه
time.sleep(2)

# ---------- اجرای اسکریپت داخل صفحه ----------
script = """
const sections = document.querySelectorAll(".card.course-lectures");
const results = [];

sections.forEach(section => {
    const header = section.querySelector(".course-lecture-header h2");
    const sectionTitle = header ? header.innerText.trim() : "بدون عنوان فصل";

    // باز کردن فصل اگر بسته است
    const collapse = section.querySelector(".course-lecture-list");
    if (collapse && collapse.classList.contains("collapse")) {
        header.parentElement.click();  // کلیک روی header
    }

    const items = section.querySelectorAll("a.video-playlist-item");
    items.forEach(item => {
        const dataIndex = item.getAttribute("data-index");
        const dataItem = item.getAttribute("data-item");
        const titleEl = item.querySelector("h3");
        const title = titleEl ? titleEl.innerText.trim() : "";
        if(title) {
            results.push({
                section: sectionTitle,
                title: title,
                dataItem: dataItem,
                dataIndex: dataIndex
            });
        }
    });
});

return results;
"""

data = driver.execute_script(script)

# ---------- نمایش ----------
for item in data:
    print(f"{item['section']} -> {item['title']} -> {item['dataItem']}")

# ---------- ذخیره به CSV ----------
os.makedirs("lectures", exist_ok=True)  # ✅ ایجاد پوشه اگر وجود ندارد
file_path = os.path.join("lectures", f"course-{course_title}.csv")

with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["section", "title", "dataItem", "dataIndex"])
    writer.writeheader()
    writer.writerows(data)

driver.quit()