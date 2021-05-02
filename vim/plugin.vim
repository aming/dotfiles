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
Plug 'vimwiki/vimwiki'
let g:vimwiki_list = [{'syntax': 'markdown','ext': '.md'}]
command! -nargs=1 VimwikiSearch Ack <args> ~/vimwiki/*.md
nnoremap <Leader>wack :VimwikiSearch

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
let g:airline#extensions#coc#enabled = 1

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
" fzf
""""""""""""""""""""""""""""""
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
nnoremap <silent> <C-p> :FZF<CR>

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
if executable('ag')
  let g:ackprg = 'ag --vimgrep'
endif

""""""""""""""""""""""""""""""
" table-mode
""""""""""""""""""""""""""""""
Plug 'dhruvasagar/vim-table-mode'

""""""""""""""""""""""""""""""
" Conquer of Completion
""""""""""""""""""""""""""""""
Plug 'neoclide/coc.nvim', {'branch': 'release'}
" Use `[c` and `]c` to navigate diagnostics
nmap <silent> [c <Plug>(coc-diagnostic-prev)
nmap <silent> ]c <Plug>(coc-diagnostic-next)
" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)
" Use K to show documentation in preview window
nnoremap <silent> K :call <SID>show_documentation()<CR>
function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction
" Highlight symbol under cursor on CursorHold
autocmd CursorHold * silent call CocActionAsync('highlight')
" Remap for rename current word
nmap <leader>rn <Plug>(coc-rename)
" Remap for format selected region
vmap <leader>f <Plug>(coc-format-selected)
nmap <leader>f <Plug>(coc-format-selected)
" Remap for do codeAction of selected region. E.G. `<leader>aap` for current paragraph
vmap <leader>a <Plug>(coc-codeaction-selected)
nmap <leader>a <Plug>(coc-codeaction-selected)
" Remap for do codeAction of current line
nmap <leader>ac <Plug>(coc-codeaction)
" Fix autofix problem of current line
nmap <leader>qf <Plug>(coc-fix-current)
" Use `:Format` to format current buffer
command! -nargs=0 Format :call CocAction('format')
" Use `:Fold` to fold current buffer
command! -nargs=? Fold :call CocAction('fold', <f-args>)
" Show all diagnostics
nnoremap <silent> <space>a :<C-u>CocList diagnostics<cr>
" Manage extensions
nnoremap <silent> <space>e :<C-u>CocList extensions<cr>
" Show commands
nnoremap <silent> <space>c :<C-u>CocList commands<cr>
" Find symbol of current document
nnoremap <silent> <space>o :<C-u>CocList outline<cr>
" Search workspace symbols
nnoremap <silent> <space>s :<C-u>CocList -I symbols<cr>
" Do default action for next item.
nnoremap <silent> <space>j :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent> <space>k :<C-u>CocPrev<CR>
" Resume latest coc list
nnoremap <silent> <space>p :<C-u>CocListResume<CR>

""""""""""""""""""""""""""""""
" plugin for Golang support
""""""""""""""""""""""""""""""
Plug 'fatih/vim-go'

" Initialize plugin system
call plug#end()
