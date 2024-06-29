----------------------------------------
-- A neovim configuration file for AMing
-- Maintainer:	AMing (cyberming at gmail dot com)
--
-- To use it, copy or link nvim to ~/.config/nvim
----------------------------------------

-- Set the runtime path to Dotfiles directory
vim.cmd('set runtimepath=$HOME/dotfiles/nvim,$VIMRUNTIME')
vim.cmd('let packpath=&runtimepath')

-- Import the config files
require'config.keymaps'
require'config.options'
require'config.plugins'
require'config.styles'

-- vim: ts=2 sw=2 ft=lua expandtab:
