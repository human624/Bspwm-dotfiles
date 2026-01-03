import os
import shutil

from core.utils import *
from core.ui import header

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")

def install_pacman_packages():
    clear()
    header("PACMAN PACKAGES")

    pkg = os.path.join(BASE_DIR, "packages.txt")
    if not os.path.isfile(pkg):
        log_err("packages.txt not found")
        return

    with open(pkg) as f:
        for p in f:
            p = p.strip()
            if p:
                print(f"{CYAN}→{RESET} {p}")
                run(f"sudo pacman -S {p}")

def install_ohmyzsh():
    clear()
    header("OH MY ZSH")

    # Download and run Oh My Zsh installer
    run("wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")
    run("sh install.sh")

    zsh_custom = os.environ.get("ZSH_CUSTOM", f"{HOME}/.oh-my-zsh/custom")

    # Install Powerlevel10k theme
    run(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {zsh_custom}/themes/powerlevel10k")
    
    # Install Zsh plugins
    run(f"git clone https://github.com/zsh-users/zsh-autosuggestions {zsh_custom}/plugins/zsh-autosuggestions")
    run(f"git clone https://github.com/zsh-users/zsh-syntax-highlighting {zsh_custom}/plugins/zsh-syntax-highlighting")

def install_paru():
    clear()
    header("PARU")

    if os.path.isdir("paru"):
        shutil.rmtree("paru")

    run("git clone https://aur.archlinux.org/paru.git")
    run("makepkg -si", cwd="paru")
    shutil.rmtree("paru")

def install_aur_packages():
    clear()
    header("AUR PACKAGES")

    pkg = os.path.join(BASE_DIR, "aur_packages.txt")
    if not os.path.isfile(pkg):
        log_err("aur_packages.txt not found")
        return

    with open(pkg) as f:
        for p in f:
            p = p.strip()
            if p:
                print(f"{CYAN}→{RESET} {p}")
                run(f"paru -S {p}")
