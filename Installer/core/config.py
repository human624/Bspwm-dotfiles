from pathlib import Path

# Path to the Bspwm-dotfiles repository
DOTFILES = Path(__file__).resolve().parents[2]

# Home directory of the current user
HOME = Path.home()

# Safety check
if not (DOTFILES / ".config").is_dir():
    raise RuntimeError(
        "Installer must be run from inside the Bspwm-dotfiles repository"
    )
