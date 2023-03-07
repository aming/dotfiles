local function plugins(use)

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
  require("neo-tree").setup({
    close_if_last_window = true,
  })

  --------------------
  -- Telescope
  --------------------
  use { 'nvim-telescope/telescope-fzf-native.nvim', run = 'make' }
  use { "nvim-telescope/telescope-file-browser.nvim" }
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
      },
      file_browser = {
        theme = "ivy",
        -- disables netrw and use telescope-file-browser in its place
        hijack_netrw = true,
        mappings = {
          ["i"] = {
            -- your custom insert mode mappings
          },
          ["n"] = {
            -- your custom normal mode mappings
          },
        },
      }
    }
  })
  require('telescope').load_extension('fzf')
  -- require("telescope").load_extension('file_browser')

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
  use 'tpope/vim-fugitive'

  --------------------
  -- BeanCount
  --------------------
  use 'nathangrigg/vim-beancount'

  --------------------
  -- Terraform
  --------------------
  use 'hashivim/vim-terraform'
end

print("Loading plugins from "..vim.fn.stdpath('data'))
require("packer").startup(plugins)

-- vim: ts=2 sw=2 ft=lua expandtab:
