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
export ZSH_CUSTOM=$HOME/dotfiles/zsh/oh-my-zsh-plugins
ZSH_THEME="robbyrussell"
plugins=(git osx z)
source $ZSH/oh-my-zsh.sh

# add settings specific to one system for zsh
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"

# This loads rbenv into a shell session.
if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi

# Add Heroku Toolbelt to PATH
export PATH="/usr/local/heroku/bin:$PATH"

export PATH="/usr/local/bin:$PATH"

autoload -Uz compinit
compinit

