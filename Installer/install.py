from core.utils import *
from core.ui import header, category_box
from core.install_tasks import *
from core.move_tasks import *

def install_menu():
    while True:
        clear()
        options = {
            "1": "Pacman packages",
            "2": "Oh My Zsh + Powerlevel10k",
            "3": "Install paru",
            "4": "AUR packages",
            "0": "Back"
        }
        category_box("INSTALLATION", options)
        choice = input("\n> ")
        if choice == "1": install_pacman_packages()
        elif choice == "2": install_ohmyzsh()
        elif choice == "3": install_paru()
        elif choice == "4": install_aur_packages()
        elif choice == "0": return
        pause()

def move_menu():
    while True:
        clear()
        options = {
            "1": "Create directories",
            "2": "Move dotfiles",
            "3": "Install LightDM",
            "0": "Back"
        }
        category_box("FILE MANAGEMENT", options)
        choice = input("\n> ")
        if choice == "1": create_directories()
        elif choice == "2": move_dotfiles()
        elif choice == "3": install_lightdm()
        elif choice == "0": return
        pause()

def main():
    while True:
        clear()
        options = {
            "1": "Installation",
            "2": "File Management",
            "0": "Exit"
        }
        category_box("BSPWM DOTFILES INSTALLER", options)
        choice = input("\n> ")
        if choice == "1": install_menu()
        elif choice == "2": move_menu()
        elif choice == "0": break

if __name__ == "__main__":
    main()
