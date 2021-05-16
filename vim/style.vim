" All color scheme and style related configuration

" Force xterm and screen (including tmux) using color 256
if (&term =~ "xterm") || (&term =~ "screen") 
    set t_Co=256 
endif 
" Turn on True Colors if available
if has('termguicolors')
    set termguicolors
endif
" Enable features if the terminal has colors support
if &t_Co > 2 || has("gui_running")
    syntax on
    set hlsearch
    let g:material_terminal_italics = 1
    let g:material_theme_style = 'ocean'
    colorscheme material
endif

