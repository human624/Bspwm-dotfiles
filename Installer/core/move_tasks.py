import os
import shutil

from core.utils import *
from core.ui import header

HOME = os.path.expanduser("~")
DOTFILES = os.path.join(HOME, "Bspwm-dotfiles")

def create_directories():
    clear()
    header("CREATE DIRECTORIES")

    for d in ["Downloads", "Documents", "Images", "Videos", "Music", "Desktop"]:
        os.makedirs(os.path.join(HOME, d), exist_ok=True)
        log_dir(f"~/{d}")

def move_dotfiles():
    clear()
    header("MOVE DOTFILES")

    exclude = [".git", "Installer", "README.md", "LICENSE", "FireFox_config", "Demonstration"]
    config_exclude = ["LightDM", "30-touchpad.conf"]

    for item in os.listdir(DOTFILES):
        if item in exclude:
            log_skip(item)
            continue

        src = os.path.join(DOTFILES, item)
        dst = os.path.join(HOME, item)

        if item == ".config":
            os.makedirs(dst, exist_ok=True)
            for cfg in os.listdir(src):
                if cfg in config_exclude:
                    log_skip(f".config/{cfg}")
                    continue

                cfg_path = os.path.join(src, cfg)
                dst_path = os.path.join(dst, cfg)

                if os.path.isdir(cfg_path):
                    shutil.copytree(cfg_path, dst_path, dirs_exist_ok=True)
                    log_dir(f"~/.config/{cfg}")
                else:
                    shutil.copy2(cfg_path, dst_path)
                    log_file(f"~/.config/{cfg}")

            # Установим права 700 для всех файлов и папок в ~/.config
            run(f"chmod -R 700 '{dst}'")
            log_info("Permissions 700 applied to ~/.config")
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

def move_touchpad_conf():
    clear()
    header("TOUCHPAD CONFIG")

    src = os.path.join(DOTFILES, ".config", "30-touchpad.conf")
    dst_dir = "/etc/X11/xorg.conf.d/"
    dst = os.path.join(dst_dir, "30-touchpad.conf")

    if not os.path.isfile(src):
        log_err("30-touchpad.conf not found in .config")
        return

    require_root()

    # Создаем директорию если её нет
    os.makedirs(dst_dir, exist_ok=True)

    run(f"cp '{src}' '{dst}'")
    log_root(dst)
