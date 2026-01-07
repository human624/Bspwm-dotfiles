# Centralized imports for the entire project

from .utils import (
    run, require_root, log_file, log_dir, log_skip,
    log_root, log_err, log_info, clear, pause,
    RESET, BOLD, GREEN, BLUE, YELLOW, RED, MAGENTA, GRAY
)
from .ui import header, category_box
from .move_tasks import create_directories, move_dotfiles, install_lightdm, move_touchpad_conf
from .install_tasks import install_pacman_packages, install_paru, install_aur_packages
from .config import DOTFILES, HOME
from .config_loader import load_config

__all__ = [
    # utils
    "run", "require_root", "log_file", "log_dir", "log_skip",
    "log_root", "log_err", "log_info", "clear", "pause",
    "RESET", "BOLD", "GREEN", "BLUE", "YELLOW", "RED", "MAGENTA", "GRAY",
    # ui
    "header", "category_box",
    # move tasks
    "create_directories", "move_dotfiles", "install_lightdm", "move_touchpad_conf",
    # install tasks
    "install_pacman_packages", "install_paru", "install_aur_packages",
    # config
    "DOTFILES", "HOME",
    # config loader
    "load_config"
]
