HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
zstyle :compinstall filename '~/.zshrc'

autoload -Uz compinit
compinit

# aliases
[ -f "~/.dotfile/zsh/aliases" ] && source "~/.dotfile/zsh/aliases"

# prompt
[ -f "~/.dotfile/zsh/prompt" ] && source "~/.dotfile/zsh/prompt"

# add settings specific to one system for zsh
[ -f "~/.zshrc.local" ] && source "~/.zshrc.local"
