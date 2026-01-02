#!/usr/bin/env python3

import os
import subprocess
import shutil
import sys

# Paths
INSTALLER_DIR = os.path.dirname(os.path.abspath(__file__))
DOTFILES_DIR = os.path.dirname(INSTALLER_DIR)
HOME = os.path.expanduser("~")

PACMAN_LIST = os.path.join(INSTALLER_DIR, "packages.txt")
AUR_LIST = os.path.join(INSTALLER_DIR, "aur_packages.txt")

# ======================
# UTILITIES
# ======================

def pause():
    input("\nPress Enter to continue...")

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

def read_packages(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# ======================
# DEPENDENCIES
# ======================

def install_pacman_deps():
    packages = read_packages(PACMAN_LIST)
    if not packages:
        print("No packages to install (pacman)")
        return

    cmd = "sudo pacman -S --needed " + " ".join(packages)
    run_cmd(cmd)

def install_aur_deps():
    packages = read_packages(AUR_LIST)
    if not packages:
        print("No packages to install (AUR)")
        return

    # Check if yay is installed
    if shutil.which("yay") is None:
        print("yay is not installed!")
        return

    cmd = "yay -S --needed " + " ".join(packages)
    run_cmd(cmd)

def dependencies_menu():
    while True:
        print("""
[ Install Dependencies ]

1) Install via pacman
2) Install via AUR
3) Install both (pacman + AUR)
4) Go back
""")
        choice = input("Choice: ")

        if choice == "1":
            install_pacman_deps()
            pause()
        elif choice == "2":
            install_aur_deps()
            pause()
        elif choice == "3":
            install_pacman_deps()
            install_aur_deps()
            pause()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

# ======================
# HOME SETUP
# ======================

def create_home_dirs():
    dirs = [
        "Videos",
        "Documents",
        "Music",
        "Downloads",
        "Desktop",
        ".config"
    ]

    for d in dirs:
        path = os.path.join(HOME, d)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")

def move_dotfiles():
    for item in os.scandir(DOTFILES_DIR):
        # Пропускаем папку "Installer"
        if item.is_dir() and item.name == "Installer":
            continue

        # Перемещаем скрытые и обычные файлы
        src = item.path
        dst = os.path.join(HOME, item.name)

        if os.path.exists(dst):
            print(f"Already exists, skipping: {item.name}")
            continue

        # Перемещаем файл
        shutil.move(src, dst)
        print(f"Moved: {item.name}")

def home_menu():
    while True:
        print("""
[ Home Setup ]

1) Create standard directories
2) Move dotfiles from Bspwm-dotfiles
3) Go back
""")
        choice = input("Choice: ")

        if choice == "1":
            create_home_dirs()
            pause()
        elif choice == "2":
            move_dotfiles()
            pause()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

# ======================
# MAIN MENU
# ======================

def main_menu():
    while True:
        print("""
=== BSPWM DOTFILES INSTALLER ===

1) Install dependencies
2) Setup Home directories
3) Exit
""")
        choice = input("Choice: ")

        if choice == "1":
            dependencies_menu()
        elif choice == "2":
            home_menu()
        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice")

# ======================
# START
# ======================

if __name__ == "__main__":
    main_menu()
