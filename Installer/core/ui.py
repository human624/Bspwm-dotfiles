from core.utils import *

BOX_WIDTH = 40  # ширина рамки

def header(title):
    """Заголовок с аккуратной рамкой"""
    print(f"{BLUE}{BOLD}")
    print("┌" + "─" * BOX_WIDTH + "┐")
    print(f"│{title.center(BOX_WIDTH)}│")  # без лишних пробелов по краям
    print("└" + "─" * BOX_WIDTH + "┘")
    print(RESET)

def category_box(title, options):
    """Категория с аккуратной рамкой"""
    print(f"{BLUE}{BOLD}┌" + "─" * BOX_WIDTH + "┐")
    print(f"│{title.center(BOX_WIDTH)}│")
    print(f"├" + "─" * BOX_WIDTH + "┤")
    for key, desc in options.items():
        line_text = f"{key}. {desc}"
        # Выравниваем так, чтобы правая рамка была ровной
        print(f"│{line_text:<{BOX_WIDTH}}│")
    print("└" + "─" * BOX_WIDTH + "┘")
    print(RESET)
