from .colors import *


def show_menu():
    menu = f"""
    {YELLOW}[1]{RESET} - {GREEN}📚 List of Courses{RESET}
    {YELLOW}[2]{RESET} - {BLUE}🍪 Update Cookie{RESET}
    {YELLOW}[3]{RESET} - {MAGENTA}➕ Add Course{RESET}
    {YELLOW}[0]{RESET} - {RED}❌ Exit{RESET}
    """
    print(menu)

    try:
        option = int(input(f"{CYAN}Select option: {RESET}"))
        return option
    except ValueError:
        print(f"{RED}❌ Invalid input! Please enter a number.{RESET}")
        exit()