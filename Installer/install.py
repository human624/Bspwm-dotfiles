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
    exclude_dirs = ["Demonstration", "FireFox_config", "Installer", "LightDM"]  # Папки, которые не должны перемещаться
    
    for item in os.scandir(DOTFILES_DIR):
        # Пропускаем папки, которые нужно исключить
        if item.is_dir() and item.name in exclude_dirs:
            print(f"Skipping directory: {item.name}")
            continue

        # Если это папка LightDM в .config, перемещаем её файлы в /etc/lightdm/
        if item.is_dir() and item.name == "config":
            lightdm_dir = os.path.join(HOME, ".config", "LightDM")
            if os.path.isdir(lightdm_dir):
                lightdm_target_dir = "/etc/lightdm/"
                
                if not os.path.exists(lightdm_target_dir):
                    print(f"Creating directory: {lightdm_target_dir}")
                    os.makedirs(lightdm_target_dir, exist_ok=True)
                
                # Удаляем файл lightdm.conf, если он существует
                lightdm_conf = os.path.join(lightdm_target_dir, "lightdm.conf")
                if os.path.exists(lightdm_conf):
                    print(f"Removing existing {lightdm_conf}")
                    os.remove(lightdm_conf)

                # Перемещаем все файлы и папки из .config/LightDM в /etc/lightdm/
                for lightdm_item in os.scandir(lightdm_dir):
                    lightdm_src = lightdm_item.path
                    lightdm_dst = os.path.join(lightdm_target_dir, lightdm_item.name)

                    if os.path.exists(lightdm_dst):
                        print(f"Already exists, skipping: {lightdm_item.name}")
                        continue

                    shutil.move(lightdm_src, lightdm_dst)
                    print(f"Moved {lightdm_item.name} to {lightdm_target_dir}")
                continue

        # Пропускаем скрытые файлы
        if item.name.startswith('.'):
            print(f"Skipping hidden file: {item.name}")
            continue

        # Перемещаем обычные файлы
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
# SYSTEM SERVICES
# ======================

def enable_services():
    print("Enabling NetworkManager and firewalld services...")

    # Enable NetworkManager service
    run_cmd("sudo systemctl enable NetworkManager")
    run_cmd("sudo systemctl start NetworkManager")
    print("NetworkManager enabled and started.")

    # Enable firewalld service
    run_cmd("sudo systemctl enable firewalld")
    run_cmd("sudo systemctl start firewalld")
    print("firewalld enabled and started.")

def services_menu():
    while True:
        print("""
[ System Services Setup ]

1) Enable NetworkManager and firewalld
2) Go back
""")
        choice = input("Choice: ")

        if choice == "1":
            enable_services()
            pause()
        elif choice == "2":
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
3) Enable system services (NetworkManager, firewalld)
4) Exit
""")
        choice = input("Choice: ")

        if choice == "1":
            dependencies_menu()
        elif choice == "2":
            home_menu()
        elif choice == "3":
            services_menu()
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice")

# ======================
# START
# ======================

if __name__ == "__main__":
    main_menu()
