#!/usr/bin/env python3
import subprocess
import shutil

# -----------------------------
# Чтение пакетов из файлов
# -----------------------------
def read_packages(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

pacman_packages = read_packages("packages.txt")
aur_packages = read_packages("aur_packages.txt")

# -----------------------------
# Функции установки
# -----------------------------
def is_installed(pkg):
    result = subprocess.run(
        ["pacman", "-Qi", pkg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def install(pkg):
    print(f"📦 Установка: {pkg} ...")
    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", pkg])

def install_aur(pkg):
    print(f"🌟 Установка AUR: {pkg} ...")
    subprocess.run(["yay", "-S", "--noconfirm", pkg])

def ask_install(packages_list, manager="pacman"):
    print(f"\nСписок пакетов для {manager}:")
    for pkg in packages_list:
        print(f"  - {pkg}")
    choice = input("\nУстановить все эти пакеты? [Y/n]: ").strip().lower()
    if choice in ["y", "yes", ""]:
        return True
    else:
        print(f"\n⚠ Пакеты {manager} не установлены из-за отказа пользователя.")
        return False

# -----------------------------
# Основной код
# -----------------------------
def main():
    print("🚀 Автоматическая установка пакетов\n")

    if shutil.which("pacman") is None:
        print("❌ Ошибка: эта система не использует pacman!")
        return

    # -----------------------------
    # Спрашиваем, какие пакеты ставить
    # -----------------------------
    print("Какие пакеты устанавливать?")
    print("1) pacman")
    print("2) AUR")
    print("3) оба сразу")
    choice = input("Выберите опцию [1/2/3]: ").strip()

    if choice not in ["1", "2", "3"]:
        print("❌ Неверный выбор. Выход.")
        return

    # -----------------------------
    # Установка pacman пакетов
    # -----------------------------
    if choice in ["1", "3"] and pacman_packages:
        if ask_install(pacman_packages, "pacman"):
            for pkg in pacman_packages:
                if is_installed(pkg):
                    print(f"✔ Уже установлен: {pkg}")
                else:
                    install(pkg)

    # -----------------------------
    # Установка AUR пакетов
    # -----------------------------
    if choice in ["2", "3"] and aur_packages:
        if shutil.which("yay") is None:
            print("\n⚠ AUR пакеты указаны, но yay не найден! Установите yay и повторите.")
        else:
            if ask_install(aur_packages, "AUR"):
                for pkg in aur_packages:
                    install_aur(pkg)

    print("\n🎉 Готово! Все выбранные пакеты обработаны.")

if __name__ == "__main__":
    main()
