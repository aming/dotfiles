" All plugins for vim managed by Vundle

set rtp+=~/dotfiles/vim/bundle/Vundle.vim
call vundle#begin("~/dotfiles/vim/bundle/myBundle")

" let Vundle manage Vundle required! 
Plugin 'VundleVim/Vundle.vim'

""""""""""""""""""""""""""""""
" My Bundles here:
" original repos on github
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" NERDTree & NERDTree-tabs
""""""""""""""""""""""""""""""
Plugin 'scrooloose/nerdtree'
let NERDTreeWinSize = 35
Plugin 'jistr/vim-nerdtree-tabs'
map <Leader>n <plug>NERDTreeTabsToggle<CR>

""""""""""""""""""""""""""""""
" Color Scheme
""""""""""""""""""""""""""""""
Plugin 'tpope/vim-vividchalk'

""""""""""""""""""""""""""""""
" Notes
""""""""""""""""""""""""""""""
Plugin 'xolox/vim-notes'
Plugin 'vim-misc'
:let g:notes_directories = ['~/Documents/Notes']

""""""""""""""""""""""""""""""
" matchit
""""""""""""""""""""""""""""""
Plugin 'matchit.zip'

""""""""""""""""""""""""""""""
" Super Tab
""""""""""""""""""""""""""""""
Plugin 'ervandew/supertab'

""""""""""""""""""""""""""""""
" plugins from tpope
""""""""""""""""""""""""""""""
Plugin 'tpope/vim-speeddating'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-unimpaired'
Plugin 'tpope/vim-commentary'
Plugin 'tpope/vim-repeat'
Plugin 'tpope/vim-endwise'

""""""""""""""""""""""""""""""
" vim-fugitive
""""""""""""""""""""""""""""""
Plugin 'tpope/vim-fugitive'
" Delete the buffer when close git object using fugitive
autocmd BufReadPost fugitive://* set bufhidden=delete
set statusline=%<%f\ %h%m%r%{fugitive#statusline()}%=%-14.(%l,%c%V%)\ %P

""""""""""""""""""""""""""""""
" hive.vim
""""""""""""""""""""""""""""""
Plugin 'autowitch/hive.vim'

""""""""""""""""""""""""""""""
" vim-dash
""""""""""""""""""""""""""""""
Plugin 'rizzatti/dash.vim'

""""""""""""""""""""""""""""""
" vim-airline
""""""""""""""""""""""""""""""
Plugin 'bling/vim-airline'
let g:airline#extensions#tabline#enabled = 1

""""""""""""""""""""""""""""""
" majutsushi/tagbar
""""""""""""""""""""""""""""""
Plugin 'majutsushi/tagbar'
" For Taglist
" configure tags - add additional tags here or comment out not-used ones
" set tags+=./ctags;,~/.vim/tags/cpp,~/.vim/tags/cpp_boost
" set tags+=./ctags;,~/.vim/tags/cpp,~/vimfiles/tags/cpp
" build tags of your own project with CTRL+F8
"map <C-F8> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+qf .<CR>
nmap <F8> :TagbarToggle<CR>

""""""""""""""""""""""""""""""
" vim-javascript
""""""""""""""""""""""""""""""
Plugin 'pangloss/vim-javascript'
Plugin 'mxw/vim-jsx'

""""""""""""""""""""""""""""""
" For ruby and rails
""""""""""""""""""""""""""""""
Plugin 'vim-ruby/vim-ruby'
Plugin 'tpope/vim-rails'
let g:rubycomplete_buffer_loading = 1
let g:rubycomplete_classes_in_global = 1
let g:rubycomplete_rails = 1

""""""""""""""""""""""""""""""
" Ctrl-P
""""""""""""""""""""""""""""""
Plugin 'ctrlpvim/ctrlp.vim'
let g:ctrlp_map = '<leader>t'
"let g:ctrlp_cmd = 'CtrlP'

""""""""""""""""""""""""""""""
" Emmet-vim
""""""""""""""""""""""""""""""
Plugin 'mattn/emmet-vim'
let g:user_emmet_mode='a'    "only enable normal mode functions.
"let g:user_emmet_mode='inv'  "enable all functions, which is equal to 'a'

""""""""""""""""""""""""""""""
" vim-mason
""""""""""""""""""""""""""""""
Plugin 'aming/vim-mason'

""""""""""""""""""""""""""""""
" ack.vim
""""""""""""""""""""""""""""""
Plugin 'mileszs/ack.vim'
let g:ackprg = 'ag --nogroup --nocolor --colum'

""""""""""""""""""""""""""""""
" End of Bundle
" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
""""""""""""""""""""""""""""""

