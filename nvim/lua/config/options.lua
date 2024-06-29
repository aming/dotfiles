-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local options = {
  backup = false,                         -- Don't creates a backup file
  swapfile = false,                       -- creates a swapfile
  fileencoding = "utf-8",                 -- the encoding written to a file
  mouse = 'a',                            -- Enable mouse operation

  cmdheight = 2,                          -- more space in the neovim command line for displaying messages
  showcmd = true,                         -- Display incomplete commands
  wildmenu = true,                        -- Enable command-line completion operation
  pumheight = 10,                         -- pop up menu height
  signcolumn = "yes",                     -- Always shows Sign column to avoid shifting (Default: Auto)
  number = true,                          -- Show line numbers
  relativenumber = false,                 -- Set relative numbered lines
  numberwidth = 2,                        -- set number column width to 2 {default 4}
  colorcolumn = '120',                    -- Set a vertical line on the 120 coloumn
  wrap = false,                           -- display lines as one long line
  scrolloff = 2,                          -- Minimum number of lines be kept above and below the cursor
  sidescrolloff = 4,                      -- Minimum number of column be kept to the right
  cursorline = true,                      -- highlight the current line

  splitbelow = true,                      -- force all horizontal splits to go below current window
  splitright = true,                      -- force all vertical splits to go to the right of current window

  ignorecase = true,                      -- Case-insensitive search
  smartcase = true,                       -- Ignore 'ignorecase' if the search pattern contains upper case
  hlsearch = true,                        -- highlight all matches on previous search pattern

  expandtab = true,                       -- Replace tabs to spaces
  smarttab = true,                        -- <BS> delete a shiftwidth
  showtabline = 2,                        -- always show tabs
  tabstop = 2,                            -- Set the tab stop
  shiftwidth = 2,                         -- the number of spaces inserted for each indentation
  smartindent = true,                     -- Autoindenting when starting a new line

  completeopt = { "menuone", "noselect" },-- mostly just for cmp
}

for k, v in pairs(options) do
  vim.opt[k] = v
end

-- vim: ts=2 sw=2 ft=lua expandtab:
