from core.utils import RESET, BOLD, BLUE

BOX_WIDTH = 40  # width of the box

def header(title):
    """Print a header with a nice box."""
    print(f"{BLUE}{BOLD}")
    print("┌" + "─" * BOX_WIDTH + "┐")
    print(f"│{title.center(BOX_WIDTH)}│")
    print("└" + "─" * BOX_WIDTH + "┘")
    print(RESET)

def category_box(title, options):
    """Print a category with options in a box."""
    print(f"{BLUE}{BOLD}┌" + "─" * BOX_WIDTH + "┐")
    print(f"│{title.center(BOX_WIDTH)}│")
    print("├" + "─" * BOX_WIDTH + "┤")
    for key, desc in options.items():
        line_text = f"{key}. {desc}"
        print(f"│{line_text:<{BOX_WIDTH}}│")
    print("└" + "─" * BOX_WIDTH + "┘")
    print(RESET)
