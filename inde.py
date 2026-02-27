# import csv
# import os
#
# # مسیر فایل CSV
# file_path = os.path.join('data', "config.csv")
# os.makedirs(os.path.dirname(file_path), exist_ok=True)
#
# # داده‌هایی که می‌خوای اضافه بشه
# data = [
#     {"key": "username", "value": "admin"},
#     {"key": "password", "value": "123456"},
#     {"key": "theme", "value": "dark"}
# ]
#
# # بررسی می‌کنیم فایل وجود داره یا نه
# file_exists = os.path.isfile(file_path)
#
# # باز کردن فایل در حالت append یا write
# with open(file_path, "a", encoding="utf-8-sig", newline="") as f:
#     writer = csv.DictWriter(f, fieldnames=["key", "value"])
#
#     # اگر فایل تازه ساخته شده، هدر بنویس
#     writer.writeheader()
#
#     # اضافه کردن داده‌ها
#     writer.writerows(data)
#

import os
import csv
import time
from utils.colors import *
import utils.banners
from utils.menu import show_menu
from actions import get_course_action


def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


option = show_menu()

if option == 1:
    get_course_action.execute()
elif option == 2:
    print(f"{YELLOW}🍪 Cookie update feature coming soon!{RESET}")
elif option == 3:
    print(f"{YELLOW}🍪 Cookie update feature coming soon!{RESET}")
elif option == 0:
    print(f"{RED}👋 Bye!{RESET}")
else:
    print(f"{RED}❌ Invalid option selected!{RESET}")
