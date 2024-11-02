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
    lazy = true,
    cmd = { 'Telescope' },
    keys = {
      { '<C-p>', ':Telescope find_files<CR>' },
      { '<C-g>', ':Telescope live_grep<CR>' },
      { '<leader>t', ':Telescope<CR>' },
      { '<leader>tr', ':Telescope resume<CR>' },
      { '<leader>ts', ':Telescope grep_string<CR>' },
      { '<leader>tb', ':Telescope buffers<CR>' },
      { '<leader>to', ':Telescope oldfiles<CR>' },
      { '<leader>tc', ':Telescope quickfix<CR>' },
      { '<leader>tj', ':Telescope jumplist<CR>' },
      { '<leader>th', ':Telescope help_tags<CR>' },
      { '<leader>tm', ':Telescope marks<CR>' },
      { '<leader>tt', ':Telescope treesitter<CR>' },
      { '<leader>tk', ':Telescope keymaps<CR>' },
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

