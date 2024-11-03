--------------------
-- NeoGit
-- https://github.com/NeogitOrg/neogit
--------------------
return {
  "NeogitOrg/neogit",
  dependencies = {
    "nvim-lua/plenary.nvim",         -- required
    "sindrets/diffview.nvim",        -- optional - Diff integration
    "nvim-telescope/telescope.nvim", -- optional
  },
  config = true,
  cmd = { 'Neogit' },
  keys = {
    { '<leader>gg', ':Neogit<CR>' },
  },
  opts = {
    extensions = {
      lazy_nvim = true,
    },
  },
}
