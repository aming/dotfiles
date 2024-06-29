--------------------
-- LSP settings
--------------------
return {
  {
    'nvim-treesitter/nvim-treesitter',
    build = ':TSUpdate'
  },
  'neovim/nvim-lspconfig',           -- Collection of configurations for built-in LSP client
  {
    'hrsh7th/nvim-cmp',              -- Autocompletion plugin
    dependencies = {
      'hrsh7th/cmp-nvim-lsp',        -- LSP source for nvim-cmp
      'hrsh7th/cmp-buffer',
    },
  },
}
