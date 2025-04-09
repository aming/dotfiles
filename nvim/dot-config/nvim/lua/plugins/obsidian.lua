--------------------
-- Obsidian
-- https://github.com/epwalsh/obsidian.nvim
--------------------

-- If you want to use the home shortcut '~' here you need to call 'vim.fn.expand'.
local personaVaultPath = vim.fn.expand '~' .. '/Notes/Personal/'
local workVaultPath = vim.fn.expand '~' .. '/Notes/Work/'

return {
  "epwalsh/obsidian.nvim",
  version = "*",  -- recommended, use latest release instead of latest commit
  ft = { 'markdown' },
  -- Only want to load obsidian.nvim for markdown files in your vault:
  event = {
    'BufReadPre ' .. personaVaultPath .. '**/*.md',
    'BufNewFile ' .. personaVaultPath .. '**/*.md',
    'BufReadPre ' .. workVaultPath .. '**/*.md',
    'BufNewFile ' .. workVaultPath .. '**/*.md',
  },
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  keys = {
    { '<leader>od', ':ObsidianToday<CR>', desc = 'obsidian [d]aily' },
    { '<leader>ot', ':ObsidianToday 1<CR>', desc = 'obsidian [t]omorrow' },
    { '<leader>oy', ':ObsidianToday -1<CR>', desc = 'obsidian [y]esterday' },
    { '<leader>ob', ':ObsidianBacklinks<CR>', desc = 'obsidian [b]acklinks' },
    { '<leader>ol', ':ObsidianLink<CR>', desc = 'obsidian [l]ink selection' },
    { '<leader>of', ':ObsidianFollowLink<CR>', desc = 'obsidian [f]ollow link' },
    { '<leader>on', ':ObsidianNew<CR>', desc = 'obsidian [n]ew' },
    { '<leader>os', ':ObsidianSearch<CR>', desc = 'obsidian [s]earch' },
    { '<leader>oo', ':ObsidianQuickSwitch<CR>', desc = 'obsidian [o]pen quickswitch' },
    { '<leader>oO', ':ObsidianOpen<CR>', desc = 'obsidian [O]pen in app' },
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
    new_notes_location = '/+',
    conceallevel = 1,
  },
}
