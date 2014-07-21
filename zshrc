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
for file in $HOME/dotfiles/zsh/lib/*; do
  source $file
done


#==================== oh-my-zsh configuration ====================#
# Path to your oh-my-zsh installation.
export ZSH=$HOME/dotfiles/zsh/oh-my-zsh
ZSH_THEME="robbyrussell"
plugins=(git)
source $ZSH/oh-my-zsh.sh


#==================== oh-my-zsh configuration ====================#
# add settings specific to one system for zsh
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

# This loads RVM into a shell session.
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

# Add RVM to PATH for scripting
export PATH="$HOME/.rvm/bin:$PATH"
# Add Heroku Toolbelt to PATH
export PATH="/usr/local/heroku/bin:$PATH"

export PATH="/usr/local/bin:$PATH"

autoload -Uz compinit
compinit

