--------------------
-- Telescope
-- https://github.com/nvim-telescope/telescope.nvim
--------------------
return {
  {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
      'nvim-lua/plenary.nvim',  -- required dependencies
      {
        'nvim-telescope/telescope-fzf-native.nvim',
        build = 'make'
      },
      'nvim-telescope/telescope-ui-select.nvim',  -- Allow nvim core to use telescope picker
      'nvim-tree/nvim-web-devicons',
      'nvim-treesitter/nvim-treesitter',
    },
    config = function()
      require('telescope').setup {
        defaults = {
          layout_strategy = 'horizontal',
          layout_config = {
            width = 0.9,
            prompt_position = 'bottom',
          },
          sorting_strategy = 'ascending',
        },
        extensions = {
          fzf = {
            fuzzy = true,                     -- false will only do exact matching
            override_generic_sorter = true,
            override_file_sorter = true,
            case_mode = 'smart_case',         -- smart_case, ignore_case or respect_case
          },
          ['ui-select'] = { require('telescope.themes').get_dropdown() },
        },
      }
      require('telescope').load_extension('fzf')
      require('telescope').load_extension('ui-select')
    end,
  },
}

