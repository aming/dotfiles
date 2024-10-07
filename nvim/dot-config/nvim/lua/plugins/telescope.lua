--------------------
-- Telescope
-- https://github.com/nvim-telescope/telescope.nvim
--------------------
return {
  {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
      'nvim-telescope/telescope-ui-select.nvim',
      'nvim-lua/plenary.nvim',
      {
        'nvim-telescope/telescope-fzf-native.nvim',
        build = 'make'
      },
    },
    opts = {
      defaults = {
        layout_strategy = 'horizontal',
        layout_config = { prompt_position = 'top' },
        sorting_strategy = 'ascending',
        winblend = 0,
      },
    },
    config = function()
      require('telescope').setup {
        extensions = {
          fzf = {
            fuzzy = true,
            override_generic_sorter = true,
            override_file_sorter = true,
            case_mode = 'smart_case',
          },
          ['ui-select'] = { require('telescope.themes').get_dropdown() },
        },
        vimgrep_argument = { 'rg', '--smart-case' },
      }
      require('telescope').load_extension 'fzf'
      require('telescope').load_extension 'ui-select'
    end,
  },
}

