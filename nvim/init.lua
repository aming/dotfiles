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

require'plugins'
require'styles'
require'lsp'
require'user.options'

-- vim: ts=2 sw=2 ft=lua expandtab:
