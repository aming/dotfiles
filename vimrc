" Source a dotfiles configuration
source $HOME/dotfiles/vim/vimrc

" Source a local configuration
if filereadable( $HOME."/.vimrc.local" )
    source $HOME/.vimrc.local
endif
