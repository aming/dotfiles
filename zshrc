# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
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
plugins=(rbenv git osx z zsh-autosuggestions pyenv zsh-syntax-highlighting tmux fzf)
source $ZSH/oh-my-zsh.sh

# add settings specific to one system for zsh
[ -f "$HOME/.config/.zshrc" ] && source "$HOME/.config/.zshrc"

# Use vim as the default editor
export EDITOR="vim"

autoload -Uz compinit
compinit

# iTerm2 Shell integration script
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# To customize prompt, run `p10k configure` or edit ~/dotfiles/zsh/p10k.zsh.
[[ ! -f ~/dotfiles/zsh/p10k.zsh ]] || source ~/dotfiles/zsh/p10k.zsh
