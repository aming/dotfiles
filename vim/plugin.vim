" All plugins for vim managed by vim-plug
" https://github.com/junegunn/vim-plug

call plug#begin('~/dotfiles/vim/plugged')

""""""""""""""""""""""""""""""
" NERDTree & NERDTree-tabs
""""""""""""""""""""""""""""""
Plug 'scrooloose/nerdtree'
let NERDTreeWinSize = 35
Plug 'jistr/vim-nerdtree-tabs'
map <Leader>n <plug>NERDTreeTabsToggle<CR>

""""""""""""""""""""""""""""""
" Color Scheme
""""""""""""""""""""""""""""""
Plug 'tpope/vim-vividchalk'

""""""""""""""""""""""""""""""
" Notes
""""""""""""""""""""""""""""""
Plug 'vim-scripts/vim-misc'
Plug 'xolox/vim-notes'
:let g:notes_directories = ['~/Documents/Notes']

""""""""""""""""""""""""""""""
" matchit
""""""""""""""""""""""""""""""
Plug 'vim-scripts/matchit.zip'

""""""""""""""""""""""""""""""
" plugins from tpope
""""""""""""""""""""""""""""""
Plug 'tpope/vim-speeddating'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-unimpaired'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-repeat'
Plug 'tpope/vim-endwise'

""""""""""""""""""""""""""""""
" vim-fugitive
""""""""""""""""""""""""""""""
Plug 'tpope/vim-fugitive'
" Delete the buffer when close git object using fugitive
autocmd BufReadPost fugitive://* set bufhidden=delete
set statusline=%<%f\ %h%m%r%{fugitive#statusline()}%=%-14.(%l,%c%V%)\ %P

""""""""""""""""""""""""""""""
" hive.vim
""""""""""""""""""""""""""""""
Plug 'autowitch/hive.vim', {'for': 'hive'}

""""""""""""""""""""""""""""""
" vim-dash
""""""""""""""""""""""""""""""
Plug 'rizzatti/dash.vim'

""""""""""""""""""""""""""""""
" vim-airline
""""""""""""""""""""""""""""""
Plug 'bling/vim-airline'
let g:airline#extensions#tabline#enabled = 1

""""""""""""""""""""""""""""""
" majutsushi/tagbar
""""""""""""""""""""""""""""""
Plug 'majutsushi/tagbar'
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
Plug 'pangloss/vim-javascript', {'for': 'javascript'}
Plug 'mxw/vim-jsx', {'for': 'javascript'}

""""""""""""""""""""""""""""""
" For ruby and rails
""""""""""""""""""""""""""""""
Plug 'vim-ruby/vim-ruby', {'for': 'ruby'}
Plug 'tpope/vim-rails', {'for': 'ruby'}
let g:rubycomplete_buffer_loading = 1
let g:rubycomplete_classes_in_global = 1
let g:rubycomplete_rails = 1

""""""""""""""""""""""""""""""
" Ctrl-P
""""""""""""""""""""""""""""""
Plug 'ctrlpvim/ctrlp.vim'
let g:ctrlp_map = '<leader>t'
"let g:ctrlp_cmd = 'CtrlP'

""""""""""""""""""""""""""""""
" Emmet-vim
""""""""""""""""""""""""""""""
Plug 'mattn/emmet-vim'
let g:user_emmet_mode='a'    "only enable normal mode functions.
"let g:user_emmet_mode='inv'  "enable all functions, which is equal to 'a'

""""""""""""""""""""""""""""""
" vim-mason
""""""""""""""""""""""""""""""
Plug 'aming/vim-mason', {'for': 'mason'}

""""""""""""""""""""""""""""""
" ack.vim
""""""""""""""""""""""""""""""
Plug 'mileszs/ack.vim'
let g:ackprg = 'ag --nogroup --nocolor --colum'

""""""""""""""""""""""""""""""
" table-mode
""""""""""""""""""""""""""""""
Plug 'dhruvasagar/vim-table-mode'

""""""""""""""""""""""""""""""
" Conquer of Completion
""""""""""""""""""""""""""""""
Plug 'neoclide/coc.nvim', {'branch': 'release'}
" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

""""""""""""""""""""""""""""""
" plugin for Golang support
""""""""""""""""""""""""""""""
Plug 'fatih/vim-go'

" Initialize plugin system
call plug#end()
