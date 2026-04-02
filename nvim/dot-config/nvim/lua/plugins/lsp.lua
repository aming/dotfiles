--------------------
-- LSP settings
--------------------
return {
  {
    -- Collection of configurations for neovim LSP client
    -- https://github.com/neovim/nvim-lspconfig
    'neovim/nvim-lspconfig',
    cmd = { 'LspInfo', 'LspInstall', 'LspStart' },
    event = { 'BufReadPre', 'BufNewFile' },
    dependencies = {
      { 'mason-org/mason.nvim', opts = {} },
      { 'mason-org/mason-lspconfig.nvim', opts = {} },
    },
  },
  {
    'nvimtools/none-ls.nvim', -- Inject LSP diagnostics, code actions to Neovim
    dependencies = {
      'nvim-lua/plenary.nvim',
    },
    config = function()
      local null_ls = require("null-ls")
      null_ls.setup({
        sources = {
          null_ls.builtins.formatting.stylua,
          null_ls.builtins.formatting.prettier,
          null_ls.builtins.diagnostics.erb_lint,
        },
      })
    end,
  },
}
