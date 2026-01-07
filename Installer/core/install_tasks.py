from core import run, clear, header
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]

# ── Read packages from file
def read_packages(file: Path):
    return [p for p in file.read_text().splitlines() if p.strip()]

def install_pacman_packages():
    clear()
    header("PACMAN PACKAGES")
    for pkg in read_packages(BASE_DIR / "packages.txt"):
        print(f"→ {pkg}")
        run(f"pacman -S --needed {pkg}", sudo=True)

    # After installing packages, create symlink for Thunar terminal
    run("ln -sf /usr/bin/alacritty /usr/bin/xterm", sudo=True)
    print("→ Symbolic link /usr/bin/xterm → /usr/bin/alacritty created for Thunar")

def install_paru():
    clear()
    header("PARU")
    if Path("paru").exists():
        shutil.rmtree("paru")
    run("git clone https://aur.archlinux.org/paru.git")
    run("makepkg -si", cwd="paru")
    shutil.rmtree("paru")

def install_aur_packages():
    clear()
    header("AUR PACKAGES")
    for pkg in read_packages(BASE_DIR / "aur_packages.txt"):
        print(f"→ {pkg}")
        run(f"paru -S --needed {pkg}")
