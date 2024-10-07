-- Styles related settings

vim.o.termguicolors = true
vim.o.background = 'dark'                       -- For dark or light version.

-- Gruvbox-Material colorScheme settings
vim.g.gruvbox_material_background = 'hard'      -- Set contrast: 'hard', 'medium', 'soft'
vim.g.gruvbox_material_foreground = 'mix'       -- Foreground color palette: 'material', 'mix', 'original'
vim.g.gruvbox_material_better_performance = 1   -- For better performance
vim.g.gruvbox_material_enable_bold = 1          -- Bold in function name
vim.cmd('colorscheme gruvbox-material')

-- vim: ts=2 sw=2 ft=lua expandtab:
