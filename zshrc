# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

HISTFILE=~/.histfile
HISTSIZE=5000
SAVEHIST=1000
setopt HIST_IGNORE_DUPS EXTENDED_HISTORY HIST_EXPIRE_DUPS_FIRST SHARE_HISTORY
bindkey -e
zstyle :compinstall filename '~/.zshrc'

#==================== zsh options ====================#
setopt AUTO_PUSHD     # auto pushd on every cd

#==================== oh-my-zsh configuration ====================#
# Path to your oh-my-zsh installation.
export ZSH=$HOME/dotfiles/zsh/oh-my-zsh
export ZSH_CUSTOM=$HOME/dotfiles/zsh/oh-my-zsh-plugins
ZSH_THEME="powerlevel10k/powerlevel10k"
HYPHEN_INSENSITIVE="true"
plugins=(rbenv pyenv nvm git osx z zsh-autosuggestions zsh-syntax-highlighting tmux fzf thefuck)
source $ZSH/oh-my-zsh.sh

# add settings specific to one system for zsh
[ -f "$HOME/.config/zshrc" ] && source "$HOME/.config/zshrc"

# Use vim as the default editor
export EDITOR="vim"

autoload -Uz compinit
compinit

# iTerm2 Shell integration script
[ -f "$HOME/.iterm2_shell_integration.zsh" ] && source "$HOME/.iterm2_shell_integration.zsh"

# To customize prompt, run `p10k configure` or edit ~/dotfiles/zsh/p10k.zsh.
[ -f "$HOME/dotfiles/zsh/p10k.zsh" ] && source "$HOME/dotfiles/zsh/p10k.zsh"

# fzf settings
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --preview "bat --style=numbers --color=always --line-range :500 {}"'
export FZF_DEFAULT_COMMAND='rg --files --no-ignore-vcs --hidden'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND="fd -t d"

# exa settings
alias ls='exa -F'
alias ll='exa -lbF --git --sort=modified'
alias llx='exa -lbhHigUmuSa --time-style=long-iso --git --color-scale'
alias tree='exa -T --level=3'

# Use Homebrew version
export PATH="/usr/local/sbin:$PATH"

