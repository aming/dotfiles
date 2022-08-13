local function plugins(use)
  local opts = { noremap=true, silent=true }

  --------------------
  -- Colorscheme
  --------------------
  use { "sainnhe/gruvbox-material" }

  --------------------
  -- Status Line
  --------------------
  use {
    'nvim-lualine/lualine.nvim',
    requires = { 'kyazdani42/nvim-web-devicons', opt = true }
  }

  --------------------
  -- Neo Tree
  --------------------
  vim.g.neo_tree_remove_legacy_commands = 1 -- Unless you are still migrating, remove deprecated commands from v1.x
  use {
  "nvim-neo-tree/neo-tree.nvim",
    branch = "v2.x",
    requires = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      { "kyazdani42/nvim-web-devicons", opt = true }, -- not strictly required, but recommended
    }
  }
  vim.keymap.set('n', '<leader>n', '<cmd>Neotree toggle left<cr>', opts)
  require("neo-tree").setup({
    close_if_last_window = true,
  })

  --------------------
  -- Telescope
  --------------------
  use { 'nvim-telescope/telescope-fzf-native.nvim', run = 'make' }
  use {
    'nvim-telescope/telescope.nvim', tag = '0.1.0',
    requires = { {'nvim-lua/plenary.nvim'} }
  }
  require('telescope').setup({
    extensions = {
      fzf = {
        fuzzy = true,                    -- false will only do exact matching
        override_generic_sorter = true,  -- override the generic sorter
        override_file_sorter = true,     -- override the file sorter
        case_mode = "smart_case",        -- "smart_case" or "ignore_case" or "respect_case"
      }
    }
  })
  require('telescope').load_extension('fzf')
  vim.keymap.set('n', '<C-p>', '<cmd>Telescope find_files<cr>', opts)
  vim.keymap.set('n', '<C-g>', '<cmd>Telescope live_grep<cr>', opts)
  vim.keymap.set('n', '<leader>fb', '<cmd>Telescope buffers<cr>', opts)
  vim.keymap.set('n', '<leader>fc', '<cmd>Telescope quickfix<cr>', opts)
  vim.keymap.set('n', '<leader>fgb', '<cmd>Telescope git_branches<cr>', opts)
  vim.keymap.set('n', '<leader>fgc', '<cmd>Telescope git_commits<cr>', opts)
  vim.keymap.set('n', '<leader>fgs', '<cmd>Telescope git_stash<cr>', opts)
  vim.keymap.set('n', '<leader>fh', '<cmd>Telescope help_tags<cr>', opts)
  vim.keymap.set('n', '<leader>fj', '<cmd>Telescope jumplist<cr>', opts)
  vim.keymap.set('n', '<leader>fm', '<cmd>Telescope marks<cr>', opts)
  vim.keymap.set('n', '<leader>fr', '<cmd>Telescope resume<cr>', opts)
  vim.keymap.set('n', '<leader>fs', '<cmd>Telescope search_history<cr>', opts)
  vim.keymap.set('n', '<leader>ft', '<cmd>Telescope treesitter<cr>', opts)

  --------------------
  -- LSP and Treesitter
  --------------------
  -- use 'nvim-treesitter/nvim-treesitter'
  use 'neovim/nvim-lspconfig'           -- Collection of configurations for built-in LSP client
  use 'hrsh7th/nvim-cmp'                -- Autocompletion plugin
  use 'hrsh7th/cmp-nvim-lsp'            -- LSP source for nvim-cmp

  --------------------
  -- plugins from tpope
  --------------------
  use 'tpope/vim-speeddating'
  use 'tpope/vim-surround'
  use 'tpope/vim-unimpaired'
  use 'tpope/vim-commentary'
  use 'tpope/vim-repeat'
  use 'tpope/vim-endwise'

  --------------------
  -- BeanCount
  --------------------
  use 'nathangrigg/vim-beancount'
end

print("Loading plugins from "..vim.fn.stdpath('data'))
require("packer").startup(plugins)

-- vim: ts=2 sw=2 ft=lua expandtab:
