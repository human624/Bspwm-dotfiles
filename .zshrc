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

# Source ranger-cd
source ~/.local/Bspwm/bin/zsh/ranger

# Alias
alias l="eza --tree --level=1 --icons=always --no-time --no-user --no-permissions"
alias ls="eza -a --tree --level=2 --icons=always --no-time --no-user --no-permissions"
alias la="eza -a --tree --level=1 --icons=always --no-time --no-user --no-permissions"
alias n="nano"
alias v="nvim"
alias c="clear"
alias rn="ranger-cd"

# Ctrl+Backspace delete left word
bindkey '^H' backward-kill-word

# fzf theme
source ~/.config/fzf/theme.zsh

# fzf
eval "$(fzf --zsh)"

# Powerlevel10k config
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
