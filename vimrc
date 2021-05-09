" Source a dotfiles configuration
set runtimepath=~/dotfiles/vim,$VIMRUNTIME
source $HOME/dotfiles/vim/vimrc

" Source a local configuration
if filereadable( "$HOME/.config/vim/vimrc" )
    source $HOME/.config/vim/vimrc
endif
