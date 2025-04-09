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
      'williamboman/mason-lspconfig.nvim', -- bridges mason.nvim with the nvim-lspconfig plugin
      'williamboman/mason.nvim',           -- manage external tooling such as LSP servers, DAP servers, linters, and formatters
    },
    config = function()
      local capabilities = require('cmp_nvim_lsp').default_capabilities()
      require('mason').setup({})
      require('mason-lspconfig').setup({
        -- ensure_installed = { 'lua-ls' },
        auto_installed = true,
        handlers = {
          -- this first function is the "default handler"
          -- it applies to every language server without a "custom handler"
          function(server_name)
            require('lspconfig')[server_name].setup({
              capabilities = capabilities
            })
          end,
        }
      })
    end
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

