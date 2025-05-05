--------------------
-- Completion settings and plugins
--------------------
return {
  "hrsh7th/nvim-cmp", -- A completion engine plugin for neovim
  event = "InsertEnter",
  dependencies = {
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-nvim-lsp", -- provide source from LSP client
    {
      "L3MON4D3/LuaSnip",
      dependencies = {
        "saadparwaiz1/cmp_luasnip",
        "rafamadriz/friendly-snippets",
      },
    },
    "supermaven-inc/supermaven-nvim", -- https://github.com/supermaven-inc/supermaven-nvim
  },
  config = function()
    local cmp = require("cmp")
    require("luasnip.loaders.from_vscode").lazy_load()
    require("supermaven-nvim").setup({
      disable_inline_completion = false, -- disables inline completion for use with cmp
      disable_keymaps = false,        -- disables built in keymaps for more manual control
      condition = function()
        return true
      end, -- condition to check for stopping supermaven, `true` means to stop supermaven when the condition is true.
    })
    cmp.setup({
      snippet = {
        expand = function(args)
          require("luasnip").lsp_expand(args.body)
        end,
      },
      window = {
        completion = cmp.config.window.bordered(),
        documentation = cmp.config.window.bordered(),
      },
      sources = cmp.config.sources({
        { name = "nvim_lsp" },
        { name = "luasnip" }, -- For luasnip users.
        { name = "supermaven" },
      }, { { name = "buffer" } }),
    })
  end,
}
