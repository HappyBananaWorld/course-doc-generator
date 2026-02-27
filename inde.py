import time
from utils.colors import *
import utils.banners
from utils.menu import show_menu
from actions import get_course_action, update_cookie_action
from utils.echo import echo


option = show_menu()

if option == 1:
    get_course_action.execute()
elif option == 2:
    update_cookie_action.execute()
elif option == 3:
    echo(f"{YELLOW}🍪 Cookie update feature coming soon!{RESET}")
elif option == 0:
    echo(f"{RED}👋 Bye!{RESET}")
else:
    echo(f"{RED}❌ Invalid option selected!{RESET}")
