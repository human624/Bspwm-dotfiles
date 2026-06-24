#source ~/.local/Bspwm/bin/zsh/tmux

# Powerlevel10k instant prompt
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Oh My Zsh and plugins
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(git z docker fzf zsh-syntax-highlighting zsh-autosuggestions history)

source $ZSH/oh-my-zsh.sh

# Source Ranger-cd
source ~/.local/Bspwm/bin/zsh/ranger

# Source Mpc
export MPD_HOST=127.0.0.1
export MPD_PORT=31231

# Alias
## Eza
alias l="eza --tree --level=1 --icons=always --no-time --no-user --no-permissions"
alias ls="eza -a --tree --level=2 --icons=always --no-time --no-user --no-permissions"
alias la="eza -a --tree --level=1 --icons=always --no-time --no-user --no-permissions"

## Programms
alias n="nano"
alias v="nvim"
alias c="clear"
alias rn="ranger-cd"
alias yt="sh ~/.local/Bspwm/bin/yt"

## Mpc
alias mp="mpc toggle"
alias mn="mpc next"
alias mpr="mpc prev"
alias ms="mpc status"
alias mup="mpc volume +5"
alias mdw="mpc volume -5"
alias mvl="mpc volume"

# Ctrl+Backspace delete left word
bindkey '^H' backward-kill-word

# fzf theme
source ~/.config/fzf/theme.zsh

# fzf
eval "$(fzf --zsh)"

# Powerlevel10k config
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
