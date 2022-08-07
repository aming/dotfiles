----------------------------------------
-- A neovim configuration file for AMing
-- Maintainer:	AMing (cyberming at gmail dot com)
--
-- To use it, copy or link nvim to ~/.config/nvim
----------------------------------------

-- Set the runtime path to Dotfiles directory
vim.cmd('set runtimepath=$HOME/dotfiles/nvim,$VIMRUNTIME')
vim.cmd('let packpath=&runtimepath')

vim.g.mapleader = ','           -- Change the leader key from '/' to ','

require('plugins')
require('styles')

-- Options
vim.o.showcmd = true            -- Display incomplete commands
vim.o.wildmenu = true           -- Enable command-line completion operation
vim.o.ignorecase = true         -- No case sensitive search
vim.o.smartcase = true          -- Ignore 'ignorecase' if the search pattern contains upper case
vim.o.expandtab = true          -- Replace tab with space
vim.o.smarttab = true           -- <BS> delete a shiftwidth
vim.o.smartindent = true        -- Autoindenting when starting a new line
vim.o.mouse = 'a'               -- Enable mouse operation
vim.o.number = true             -- Show line numbers
vim.o.colorcolumn = '120'       -- Set the line on the 120 coloumn


-- vim: ts=2 sw=2 ft=lua expandtab:
