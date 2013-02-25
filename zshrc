HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
zstyle :compinstall filename '~/.zshrc'

#==================== zsh options ====================#
setopt AUTO_PUSHD     # auto pushd on every cd

#==================== import other files ====================#
# aliases
[ -e "$HOME/dotfiles/zsh/aliases" ] && source "$HOME/dotfiles/zsh/aliases"

# prompt
[ -f "$HOME/dotfiles/zsh/zprompt" ] && source "$HOME/dotfiles/zsh/zprompt"

# add settings specific to one system for zsh
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

autoload -Uz compinit
compinit

