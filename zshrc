HISTFILE=~/.histfile
HISTSIZE=5000
SAVEHIST=1000
setopt HIST_IGNORE_DUPS EXTENDED_HISTORY HIST_EXPIRE_DUPS_FIRST SHARE_HISTORY
bindkey -e
zstyle :compinstall filename '~/.zshrc'

#==================== zsh options ====================#
setopt AUTO_PUSHD     # auto pushd on every cd

#==================== oh-my-zsh configuration ====================#

export DOTFILES=$HOME/dotfiles
export ZSH=$DOTFILES/zsh/oh-my-zsh  # Path to your oh-my-zsh installation.
ZSH_CUSTOM=$DOTFILES/zsh/oh-my-zsh-plugins
ZSH_THEME="powerlevel10k/powerlevel10k"

# ZSH_TMUX_AUTOSTART='true'
ZSH_TMUX_AUTOCONNECT='true'
ZSH_TMUX_FIXTERM='true'
ZSH_TMUX_UNICODE='true'
ZSH_TMUX_CONFIG="$DOTFILES/tmux/tmux.conf"

HYPHEN_INSENSITIVE='true'  # _ and - will be interchangeable.

# pyenv settings
ZSH_PYENV_QUIET='true'

# fzf settings
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --preview "bat --style=numbers --color=always --line-range :500 {}"'
export FZF_DEFAULT_COMMAND='rg --files --no-ignore-vcs --hidden'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_CTRL_R_OPTS="--no-preview"
export FZF_ALT_C_COMMAND="fd -t d . $HOME"
export FZF_ALT_C_OPTS='--height 40% --layout=reverse --border --preview-window=down --preview "ls {}"'

# zoxide settings
export _ZO_FZF_OPTS='--height 40% --layout=reverse --border --no-preview'
export _ZO_DATA_DIR=$HOME/.local/share

plugins=(brew pyenv rbenv nvm asdf git macos zsh-syntax-highlighting zsh-autosuggestions tmux fzf fzf-tab forgit thefuck zoxide)
source $ZSH/oh-my-zsh.sh

# add settings specific to one system for zsh
[ -f "$HOME/.config/zsh/zshrc" ] && source "$HOME/.config/zsh/zshrc"

# Use vim as the default editor
export EDITOR="vim"

autoload -Uz compinit
compinit

# To customize prompt, run `p10k configure` or edit $DOTFILES/zsh/p10k.zsh.
[ -f "$DOTFILES/zsh/p10k.zsh" ] && source "$DOTFILES/zsh/p10k.zsh"

# iTerm2 Shell integration script
[ -f "$HOME/.iterm2_shell_integration.zsh" ] && source "$HOME/.iterm2_shell_integration.zsh"

# exa settings
alias ls='exa -F'
alias ll='exa -lbF --git --sort=modified'
alias llx='exa -lbhHigUmuSa --time-style=long-iso --git --color-scale'
alias tree='exa -T --level=3'

# bat settings
export BAT_CONFIG_PATH="$DOTFILES/bat.config"

