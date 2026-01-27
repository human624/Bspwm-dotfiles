from core.config import DOTFILES, HOME
from core.utils import run, log_file, log_dir, log_skip, log_root, log_err, clear, require_root
from core.ui import header
from core.config_loader import load_config
from pathlib import Path
import shutil

# ── Load installer config
CONFIG_FILE = DOTFILES / "Installer" / "config.yaml"
CONFIG = load_config(CONFIG_FILE)

DIRS = CONFIG.get("directories", ["Downloads", "Documents", "Images", "Videos", "Music", "Desktop"])
EXCLUDE_ROOT = set(CONFIG.get("exclude_root", []))
EXCLUDE_CONFIG = set(CONFIG.get("exclude_config", []))

# ── Copy a file or directory
def copy_item(src: Path, dst: Path):
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
        log_dir(dst)
    else:
        shutil.copy2(src, dst)
        log_file(dst)

# ── Create standard user directories
def create_directories():
    clear()
    header("CREATE DIRECTORIES")
    for name in DIRS:
        p = HOME / name
        p.mkdir(exist_ok=True)
        log_dir(f"~/{name}")

# ── Move dotfiles from repository to home
def move_dotfiles():
    clear()
    header("MOVE DOTFILES")
    for item in DOTFILES.iterdir():
        if item.name in EXCLUDE_ROOT:
            log_skip(item.name)
            continue

        target = HOME / item.name
        if item.name == ".config":
            move_config(item, target, EXCLUDE_CONFIG)
        else:
            copy_item(item, target)

def move_config(src: Path, dst: Path, exclude):
    dst.mkdir(exist_ok=True)
    for cfg in src.iterdir():
        if cfg.name in exclude:
            log_skip(f".config/{cfg.name}")
            continue
        copy_item(cfg, dst / cfg.name)
    run(f"chmod -R 700 '{dst}'")

def install_lightdm():
    require_root()
    clear()
    header("LIGHTDM")

    # ── Wallpapers
    wp_src = DOTFILES / "Images" / "screen-lock.png"
    wp_dir = Path("/usr/share/wallpapers")
    wp_dst = wp_dir / "screen-lock.png"

    if not wp_src.exists():
        log_err("screen-lock.png not found in Images/")
    else:
        run(f"mkdir -p '{wp_dir}'", sudo=True)
        run(f"cp '{wp_src}' '{wp_dst}'", sudo=True)
        log_root(wp_dst)

    # ── LightDM config
    src = DOTFILES / ".config" / "LightDM"
    dst = Path("/etc/lightdm")

    if not src.exists():
        log_err("LightDM config not found")
        return

    run(f"cp -rT '{src}' '{dst}'", sudo=True)
    log_root(dst)

def move_touchpad_conf():
    clear()
    header("TOUCHPAD CONFIG")
    src = DOTFILES / ".config" / "30-touchpad.conf"
    dst = Path("/etc/X11/xorg.conf.d/30-touchpad.conf")
    if not src.exists():
        log_err("touchpad config not found")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(f"cp '{src}' '{dst}'", sudo=True)
    log_root(dst)
