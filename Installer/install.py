#!/usr/bin/env python3
"""
install_packages.py

Interactive package installer for Arch Linux (no CLI options).
- Reads pacman list from packages.txt
- Reads AUR list from aur_packages.txt
- Prompts at start to choose: pacman / AUR / both
- Nicely formatted adaptive banner (colors/centering/wrapping)
- Skips already installed packages (--needed)
- Auto-detects AUR helper (paru -> yay)
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
import textwrap
from typing import List, Optional, Tuple

PACMAN_FILE = "packages.txt"
AUR_FILE = "aur_packages.txt"

# ANSI colors / styles
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
DIM = CSI + "2m"
FG_CYAN = CSI + "36m"
FG_GREEN = CSI + "32m"
FG_YELLOW = CSI + "33m"
FG_RED = CSI + "31m"
FG_MAGENTA = CSI + "35m"


def term_width(default: int = 100) -> int:
    try:
        w = shutil.get_terminal_size().columns
        return max(40, min(default, w))
    except Exception:
        return default


def boxed_banner(lines: List[str], width: Optional[int] = None, color: str = "") -> None:
    """
    Draws a neat box with centering and wrapping.
    color - ANSI prefix (e.g. FG_CYAN); pass "" to disable color.
    """
    w = width or term_width()
    inner_w = w - 4  # account for box borders
    wrapped: List[str] = []
    for ln in lines:
        if ln.strip() == "":
            wrapped.append("")  # blank line as spacer
            continue
        for part in textwrap.wrap(ln, width=inner_w):
            wrapped.append(part)

    top = "╔" + "═" * (w - 2) + "╗"
    mid_sep = "╠" + "═" * (w - 2) + "╣"
    bottom = "╚" + "═" * (w - 2) + "╝"

    print(color + top + RESET)
    title_printed = False
    for ln in wrapped:
        if not title_printed and ln.strip():
            content = ln.center(w - 4)
            print(color + "║ " + BOLD + content + RESET + color + " ║" + RESET)
            title_printed = True
            print(color + mid_sep + RESET)
            continue
        content = ln.center(w - 4)
        print(color + "║ " + content + " ║" + RESET)
    print(color + bottom + RESET)


def banner() -> None:
    """
    A specific banner using the user's text, formatted nicely and colorized.
    """
    lines = [
        "Package Installer for Arch Linux",
        "",
        "- This utility automatically installs all packages required for my custom Linux build.",
        "- It prepares the system, pulls dependencies and configures the environment so it's ready to use after installation.",
        "",
        "Files: packages.txt (pacman), aur_packages.txt (AUR).",
        "This script is interactive — choose what to install at the start.",
    ]
    boxed_banner(lines, width=min(100, term_width()), color=FG_CYAN)


def read_packages(filename: str) -> List[str]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    pkgs: List[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.split("#", 1)[0].strip()
        if line:
            pkgs.append(line)
    return pkgs


def run_command(cmd: List[str], capture: bool = False) -> Tuple[int, str, str]:
    """
    Always uses text=True so stdout/stderr are str (not bytes).
    If capture=False — stdout/stderr return empty strings.
    """
    try:
        if capture:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return res.returncode, (res.stdout or "").strip(), (res.stderr or "").strip()
        else:
            res = subprocess.run(cmd, text=True)
            return res.returncode, "", ""
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, "", str(e)


def ensure_root_prefix(cmd: List[str]) -> List[str]:
    if os.geteuid() == 0:
        return cmd
    if shutil.which("sudo"):
        return ["sudo"] + cmd
    return cmd


def detect_aur_helper() -> Optional[str]:
    for h in ("paru", "yay"):
        if shutil.which(h):
            return h
    return None


def is_installed(pkg: str) -> bool:
    code, _, _ = run_command(["pacman", "-Qi", pkg], capture=True)
    return code == 0


def pretty_list(items: List[str]) -> str:
    if not items:
        return "(empty)"
    return "\n".join(f"  • {i}" for i in items)


def confirm(prompt: str) -> bool:
    try:
        resp = input(FG_YELLOW + prompt + " [Y/n]: " + RESET).strip().lower()
    except EOFError:
        return False
    return resp in ("", "y", "yes")


def install_pacman(packages: List[str]) -> None:
    if not packages:
        print(FG_MAGENTA + "ℹ No pacman packages to install." + RESET)
        return

    to_install = [p for p in packages if not is_installed(p)]
    already = [p for p in packages if p not in to_install]

    if already:
        print(FG_GREEN + "✔ Already installed (pacman):" + RESET)
        print(pretty_list(already))
    if not to_install:
        print(FG_GREEN + "✅ All pacman packages are already installed.\n" + RESET)
        return

    print(FG_CYAN + "\nPackages to install via pacman:" + RESET)
    print(pretty_list(to_install))
    if not confirm("Install these pacman packages?"):
        print(FG_RED + "⚠ Pacman package installation canceled by user.\n" + RESET)
        return

    cmd = ensure_root_prefix(["pacman", "-S", "--noconfirm", "--needed"] + to_install)
    print(FG_YELLOW + f"\n⏳ Executing: {shlex.join(cmd)}" + RESET)
    code, out, err = run_command(cmd, capture=True)
    if code == 0:
        print(FG_GREEN + "🎉 pacman: installation succeeded." + RESET)
        if out:
            print(out)
    else:
        print(FG_RED + f"❌ pacman returned exit code {code}." + RESET)
        if out:
            print("stdout:", out)
        if err:
            print("stderr:", err)
    print("")


def install_aur(packages: List[str]) -> None:
    if not packages:
        print(FG_MAGENTA + "ℹ No AUR packages to install." + RESET)
        return

    helper = detect_aur_helper()
    if not helper:
        print(FG_RED + "❗ AUR packages listed but neither paru nor yay was found." + RESET)
        print("  Please install an AUR helper (paru or yay) and try again.\n")
        return

    to_install = [p for p in packages if not is_installed(p)]
    already = [p for p in packages if p not in to_install]

    if already:
        print(FG_GREEN + "✔ Already installed (AUR/pacman DB):" + RESET)
        print(pretty_list(already))
    if not to_install:
        print(FG_GREEN + "✅ All AUR packages are already installed.\n" + RESET)
        return

    print(FG_CYAN + f"\nPackages to install via {helper}:" + RESET)
    print(pretty_list(to_install))
    if not confirm(f"Install AUR packages via {helper}?"):
        print(FG_RED + "⚠ AUR package installation canceled by user.\n" + RESET)
        return

    cmd = [helper, "-S", "--noconfirm", "--needed"] + to_install
    print(FG_YELLOW + f"\n⏳ Executing: {shlex.join(cmd)}" + RESET)
    code, out, err = run_command(cmd, capture=True)
    if code == 0:
        print(FG_GREEN + f"🎉 {helper}: installation succeeded." + RESET)
        if out:
            print(out)
    else:
        print(FG_RED + f"❌ {helper} returned exit code {code}." + RESET)
        if out:
            print("stdout:", out)
        if err:
            print("stderr:", err)
    print("")


def main() -> None:
    banner()

    if shutil.which("pacman") is None:
        print(FG_RED + "❌ Error: pacman not found. This script is intended for Arch Linux." + RESET)
        sys.exit(2)

    pacman_packages = read_packages(PACMAN_FILE)
    aur_packages = read_packages(AUR_FILE)

    # Choose manager at start
    print(BOLD + "What would you like to install?" + RESET)
    print("  1) pacman packages (from packages.txt)")
    print("  2) AUR packages (from aur_packages.txt)")
    print("  3) Both (pacman + AUR)")
    choice = input(FG_YELLOW + "Select an option [1/2/3]: " + RESET).strip()
    if choice not in ("1", "2", "3"):
        print(FG_RED + "❌ Invalid choice. Exiting." + RESET)
        return

    print("")  # blank line for readability

    if choice in ("1", "3"):
        print(FG_MAGENTA + "=== PACMAN ===" + RESET)
        if pacman_packages:
            install_pacman(pacman_packages)
        else:
            print(FG_MAGENTA + "ℹ packages.txt is empty or missing — skipping pacman.\n" + RESET)

    if choice in ("2", "3"):
        print(FG_MAGENTA + "=== AUR ===" + RESET)
        if aur_packages:
            install_aur(aur_packages)
        else:
            print(FG_MAGENTA + "ℹ aur_packages.txt is empty or missing — skipping AUR.\n" + RESET)

    print(FG_CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + RESET)
    print(FG_GREEN + "Done! All selected actions have completed." + RESET)
    print("If needed, edit packages.txt / aur_packages.txt and run again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + FG_RED + "Interrupted by user." + RESET)
        sys.exit(130)
