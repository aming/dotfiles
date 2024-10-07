--------------------
-- Obsidian
-- https://github.com/epwalsh/obsidian.nvim?tab=readme-ov-file#setup
--------------------

-- If you want to use the home shortcut '~' here you need to call 'vim.fn.expand'.
local personaVaultPath = vim.fn.expand '~' .. '/Notes/Personal/'
local workVaultPath = vim.fn.expand '~' .. '/Notes/Work/'

return {
  "epwalsh/obsidian.nvim",
  version = "*",  -- recommended, use latest release instead of latest commit
  lazy = true,
  ft = "markdown",
  -- Only want to load obsidian.nvim for markdown files in your vault:
  event = {
    'BufReadPre ' .. personaVaultPath .. '**.md',
    'BufNewFile ' .. personaVaultPath .. '**.md',
    'BufReadPre ' .. workVaultPath .. '**.md',
    'BufNewFile ' .. workVaultPath .. '**.md',
  },
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  opts = {
    workspaces = {
      {
        name = "personal",
        path = personaVaultPath,
      },
      {
        name = "work",
        path = workVaultPath,
      },
    },
    conceallevel = 1,
  },
}
