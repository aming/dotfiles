HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
zstyle :compinstall filename '~/.zshrc'

#==================== zsh options ====================#
setopt AUTO_PUSHD     # auto pushd on every cd

#==================== import other files ====================#
# import all the zsh settings
zsh_home=$HOME/dotfiles/zsh
for file in $HOME/dotfiles/zsh/*; do
  source $file
done

# add settings specific to one system for zsh
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

# This loads RVM into a shell session.
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting


autoload -Uz compinit
compinit


### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"
