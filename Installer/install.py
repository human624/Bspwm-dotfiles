from core import (
    clear, header, category_box,
    create_directories, move_dotfiles, install_lightdm, move_touchpad_conf,
    install_pacman_packages, install_paru, install_aur_packages,
    pause, HOME
)

def install_menu():
    while True:
        clear()
        options = {
            "1": "Pacman packages",
            "2": "Oh My Zsh + Powerlevel10k",
            "3": "Install paru",
            "4": "AUR packages",
            "0": "Back"
        }
        category_box("INSTALLATION", options)
        choice = input("\n> ")
        if choice == "1":
            install_pacman_packages()
        elif choice == "2":
            # Oh My Zsh installer moved inline here for simplicity
            from core import run
            clear()
            header("OH MY ZSH")
            run("wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")
            run("sh install.sh")
            zsh_custom = f"{HOME}/.oh-my-zsh/custom"
            run(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {zsh_custom}/themes/powerlevel10k")
            run(f"git clone https://github.com/zsh-users/zsh-autosuggestions {zsh_custom}/plugins/zsh-autosuggestions")
            run(f"git clone https://github.com/zsh-users/zsh-syntax-highlighting {zsh_custom}/plugins/zsh-syntax-highlighting")
        elif choice == "3":
            install_paru()
        elif choice == "4":
            install_aur_packages()
        elif choice == "0":
            return
        pause()

def move_menu():
    while True:
        clear()
        options = {
            "1": "Create directories",
            "2": "Move dotfiles",
            "3": "Install LightDM",
            "4": "Install touchpad config",
            "0": "Back"
        }
        category_box("FILE MANAGEMENT", options)
        choice = input("\n> ")
        if choice == "1":
            create_directories()
        elif choice == "2":
            move_dotfiles()
        elif choice == "3":
            install_lightdm()
        elif choice == "4":
            move_touchpad_conf()
        elif choice == "0":
            return
        pause()

def main():
    while True:
        clear()
        options = {
            "1": "Installation",
            "2": "File Management",
            "0": "Exit"
        }
        category_box("BSPWM DOTFILES INSTALLER", options)
        choice = input("\n> ")
        if choice == "1":
            install_menu()
        elif choice == "2":
            move_menu()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
