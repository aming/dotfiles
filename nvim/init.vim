" Source a dotfiles configuration
set runtimepath=$HOME/dotfiles/vim,$VIMRUNTIME
let &packpath = &runtimepath

" Source vim configuration
source $HOME/dotfiles/vim/vimrc

tnoremap <Esc> <C-\><C-n>

lua <<EOF
-- LSP setup
-- require'lspconfig'.pyright.setup{}
EOF
