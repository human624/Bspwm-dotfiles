# ✨ Bspwm-dotfiles

A **minimal, clean, and highly productive bspwm setup** designed for users who value efficiency, speed, and a smooth workflow.  
These dotfiles are lightweight, fully customizable, and ready to use — perfect for anyone who wants a **beautiful, distraction-free desktop** that helps you stay focused and get things done.  

Join hundreds of users who enjoy **fast, organized, and elegant workspace management** with this setup!

## 🖥️ System Overview

<img src="Demonstration/1.png" alt="rice" align="right" width="500px">

</br>

- **OS:** [**`EndeavourOS`**](https://endeavouros.com)
- **WM:** [**`BSPWM`**](https://github.com/baskerville/bspwm) 
- **Bar:** [**`Polybar`**](https://github.com/polybar/polybar)  
- **Compositor:** [**`Picom`**](https://github.com/yshui/picom)  
- **Terminal:** [**`Alacritty`**](https://github.com/alacritty/alacritty)  
- **Shell:** [**`Zsh`**](https://github.com/zsh-users/zsh) [**`(Oh My Zsh)`**](https://github.com/ohmyzsh/ohmyzsh)
- **App Launcher:** [**`Rofi`**](https://github.com/davatorium/rofi)  
- **Notify Daemon:** [**`Dunst`**](https://github.com/dunst-project/dunst) 

</br>

## 📸 Desktop Preview

![Desktop Screenshot](Demonstration/1.png)
![Desktop Screenshot](Demonstration/2.png)
![Desktop Screenshot](Demonstration/3.png)
![Desktop Screenshot](Demonstration/4.png)

## ⚡ Features

- ✨ **Minimal and clutter-free** bspwm setup for ultimate focus  
- ⌨️ **Efficient keybindings** via sxhkd to navigate faster  
- 🛠️ **Lightweight scripts** to enhance daily workflow  
- 🎨 **Customizable themes, fonts, and colors** for a visually appealing environment  
- 📊 **Pre-configured Polybar** for a clean, informative status bar  
- 🚀 **Optimized for speed and productivity** — perfect for work and development  
- 📦 **Organized structure** making it easy to tweak and adapt  
- 🌟 Ready-to-use configuration so you can set up your environment **in minutes**  

> ⚠️ **Note:** This configuration was primarily created and tested for a screen resolution of **1366×768**. Adjustments may be needed for other resolutions.

## ⌨️ Hotkeys

  <details>
  <summary>Hotkeys for Tmux</summary>

  ### **Quick Access to Windows**
  - `M-1` to `M-9`: Switch to window 1-9.

  ### **Pane Navigation**
  - `M-Left`: Move to the left pane.
  - `M-Right`: Move to the right pane.
  - `M-Up`: Move to the top pane.
  - `M-Down`: Move to the bottom pane.

  ### **Pane Resizing**
  - `M-C-Left`: Resize pane to the left.
  - `M-C-Right`: Resize pane to the right.
  - `M-C-Up`: Resize pane upwards.
  - `M-C-Down`: Resize pane downwards.

  ### **Window and Pane Management**
  - `M-h`: Split window vertically.
  - `M-v`: Split window horizontally.
  - `M-Enter`: Create a new window.
  - `M-c`: Close the current pane.
  - `M-q`: Close the current window.
  - `M-d`: Detach from the tmux session.
  - `M-C-q`: Confirm to kill the entire session.

  ### **Reload Configuration**
  - `M-r`: Reload tmux configuration.
  - `M-s`: Choose a tmux session tree.

  ### **Copying and Searching**
  - `M-/`: Start copy mode and search forward.
  - `M-?`: Start copy mode and search backward.
  - `v`: Begin selection in copy mode.
  - `y`: Copy selected text to clipboard.
</details>

<details>
  <summary>Hotkeys for Sxhkd</summary>

  ### **Reload Sxhkd Configuration**
  - `super + Escape + r`: Reload sxhkd configuration.

  ### **Launch Terminal and Applications**
  - `super + Return`: Open Alacritty terminal.
  - `super + d`: Open Rofi application menu.
  - `super + x`: Launch powermenu.

  ### **Volume and Brightness Control**
  - `XF86AudioRaiseVolume`: Increase volume.
  - `XF86AudioLowerVolume`: Decrease volume.
  - `XF86AudioMute`: Mute/unmute sound.
  - `XF86MonBrightnessUp`: Increase brightness.
  - `XF86MonBrightnessDown`: Decrease brightness.

  ### **Polybar and Wallpaper Management**
  - `super + p`: Toggle Polybar visibility.
  - `super + w`: Set a random wallpaper.
  - `Alt_L + Shift`: Change system language.

  ### **Application Hotkeys**
  - `super + shift + {f,n,p,i,l}`: Launch applications (Firefox, Thunar, etc.).
</details>

<details>
  <summary>Hotkeys for BSPWM</summary>

  ### **Window Management**
  - `super + space`: Toggle between tiling and floating window modes.
  - `super + {1-9}`: Move window to desktop 1-9.
  - `super + c`: Close the current window.

  ### **Focus and Navigation**
  - `alt + {_,shift + }Tab`: Switch to the next/previous window.
  - `super + {grave,Tab}`: Focus on the last active window.

  ### **Resizing and Moving**
  - `super + control {h,j,k,l}`: Resize window in the specified direction.
  - `super + {_,alt + }{h,j,k,l}`: Move window to one of the screen's sides.
</details>

<details>
  <summary>Hotkeys for Ranger</summary>

  ### **Navigation**
  - `<Up>, <Down>, <Left>, <Right>`: Navigate directories and files.
  - `<PageUp>, <PageDown>`: Scroll up/down through the file list.
  - `gg`: Go to the top of the list.
  - `G`: Go to the bottom of the list.

  ### **File Operations**
  - `yy`: Copy selected file.
  - `dd`: Cut selected file.
  - `pp`: Paste file.
  - `rr`: Rename selected file.

  ### **Search**
  - `/`: Start search.
  - `n`: Next search result.
  - `N`: Previous search result.

  ### **Image Preview**
  - `ueberzug` is used to preview images in Ranger.
</details>

## 🛠️ Installer

To make the setup process as smooth and effortless as possible, a dedicated **Installer** folder has been added.  
Inside, you'll find a **fully automated installation script** that handles all required dependencies for the complete Bspwm-dotfiles environment — from the window manager itself to essential tools, utilities, and supporting components.

All you need to do is open the **Installer** folder and run the following command:
```sh
python3 install.py
```
The script will automatically install everything you need within minutes, saving you from manually searching for, tracking, and installing each package one by one.

This provides a **fast, seamless, and hassle-free installation experience**, allowing you to dive straight into customizing and enjoying your optimized desktop environment.

## 🙏 Acknowledgements

Special thanks to **[ZProger](https://www.youtube.com/@ZProger)** for inspiration and many configuration ideas used in this setup.
