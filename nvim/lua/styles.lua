-- Styles related settings

vim.o.termguicolors = true
vim.o.background = 'dark'                       -- For dark or light version.

-- Gruvbox-Material colorScheme settings
vim.g.gruvbox_material_background = 'hard'      -- Set contrast: 'hard', 'medium', 'soft'
vim.g.gruvbox_material_foreground = 'mix'       -- Foreground color palette: 'material', 'mix', 'original'
vim.g.gruvbox_material_better_performance = 1   -- For better performance
vim.g.gruvbox_material_enable_bold = 1          -- Bold in function name
vim.cmd('colorscheme gruvbox-material')

-- Status Line setup
require('lualine').setup {
  options = {
    icons_enabled = true,
    theme = 'gruvbox-material',
    component_separators = { left = '', right = ''},
    section_separators = { left = '', right = ''},
    disabled_filetypes = {
      statusline = {},
      winbar = {},
    },
    ignore_focus = {},
    always_divide_middle = true,
    globalstatus = false,
    refresh = {
      statusline = 1000,
      tabline = 1000,
      winbar = 1000,
    }
  },
  sections = {
    lualine_a = {'mode'},
    lualine_b = {'branch', 'diff', 'diagnostics'},
    lualine_c = { {'filename', path = 1,} },
    lualine_x = {'encoding', 'fileformat', 'filetype'},
    lualine_y = {'progress'},
    lualine_z = {'location'}
  },
  inactive_sections = {
    lualine_a = {},
    lualine_b = {},
    lualine_c = {'filename'},
    lualine_x = {'location'},
    lualine_y = {},
    lualine_z = {}
  },
  tabline = {
    lualine_a = {'buffers'},
    lualine_b = {},
    lualine_c = {},
    lualine_x = {},
    lualine_y = {},
    lualine_z = {},
  },
  winbar = {},
  inactive_winbar = {},
  extensions = {}
}

-- vim: ts=2 sw=2 ft=lua expandtab:
