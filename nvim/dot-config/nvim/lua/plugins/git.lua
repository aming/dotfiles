--------------------
-- Git plugins
--------------------
return {
  {
    "NeogitOrg/neogit",                -- https://github.com/NeogitOrg/neogit
    dependencies = {
      "nvim-lua/plenary.nvim",         -- required
      "sindrets/diffview.nvim",        -- optional - Diff integration
      "nvim-telescope/telescope.nvim", -- optional
    },
    cmd = { 'Neogit' },
    config = true,
    keys = {
      { '<leader>gg', ':Neogit<CR>' },
    },
    opts = {
      extensions = {
        lazy_nvim = true,
      },
    },
  },
  {
    "lewis6991/gitsigns.nvim",
    config = function()
      require("gitsigns").setup()
      vim.keymap.set("n", "<leader>gp", ":Gitsigns preview_hunk<CR>", {})
      vim.keymap.set("n", "<leader>gt", ":Gitsigns toggle_current_line_blame<CR>", {})
    end
  },
}

