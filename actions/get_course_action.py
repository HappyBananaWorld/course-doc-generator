from utils.colors import *
import os


def execute():
    courses_path = os.path.join('data', 'lectures')
    if not os.path.exists(courses_path):
        print(f"{RED}No courses found!{RESET}")
        return

    courses = os.listdir(courses_path)
    if not courses:
        print(f"{YELLOW}No courses available yet.{RESET}")
        return

    print(f"{GREEN}{BOLD}🌟 Available Courses 🌟{RESET}")
    for idx, course in enumerate(courses, 1):
        course_name = course.replace('course-', '')
        print(f"{idx}. {MAGENTA}{course_name} 🎉{RESET}")
