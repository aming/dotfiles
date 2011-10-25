" Source a dotfiles configuration
set runtimepath=~/dotfiles/vim,$VIMRUNTIME
source $HOME/dotfiles/vim/vimrc

" Source a local configuration
if filereadable( $HOME."/.vimrc.local" )
    source $HOME/.vimrc.local
endif
