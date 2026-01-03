import os
import shutil

from core.utils import *
from core.ui import header

HOME = os.path.expanduser("~")
DOTFILES = os.path.join(HOME, "Bspwm-dotfiles")

def create_directories():
    clear()
    header("CREATE DIRECTORIES")

    for d in ["Downloads", "Documents", "Pictures", "Videos", "Music", "Desktop"]:
        os.makedirs(os.path.join(HOME, d), exist_ok=True)
        log_dir(f"~/{d}")

def move_dotfiles():
    clear()
    header("MOVE DOTFILES")

    exclude = [".git", "Installer", "README.md", "LICENSE", "FireFox_config", "Demonstration"]

    for item in os.listdir(DOTFILES):
        if item in exclude:
            log_skip(item)
            continue

        src = os.path.join(DOTFILES, item)
        dst = os.path.join(HOME, item)

        if item == ".config":
            os.makedirs(dst, exist_ok=True)
            for cfg in os.listdir(src):
                if cfg == "LightDM":
                    log_skip(".config/LightDM")
                    continue
                shutil.copytree(
                    os.path.join(src, cfg),
                    os.path.join(dst, cfg),
                    dirs_exist_ok=True
                )
                log_dir(f"~/.config/{cfg}")
        else:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
                log_dir(f"~/{item}")
            else:
                shutil.copy2(src, dst)
                log_file(f"~/{item}")

def install_lightdm():
    clear()
    header("LIGHTDM")

    src = os.path.join(DOTFILES, ".config", "LightDM")
    dst = "/etc/lightdm"

    if not os.path.isdir(src):
        log_err("LightDM configuration not found")
        return

    require_root()
    run(f"cp -rT '{src}' '{dst}'")
    log_root("/etc/lightdm")
