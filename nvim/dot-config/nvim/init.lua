----------------------------------------
-- A neovim configuration file for AMing
-- Maintainer:	AMing (cyberming at gmail dot com)
--
-- To use it, copy or link nvim to ~/.config/nvim
----------------------------------------

-- Set the runtime path to Dotfiles directory
vim.cmd('set runtimepath=$HOME/dotfiles/nvim/dot-config/nvim,$VIMRUNTIME')
vim.cmd('let packpath=&runtimepath')

-- Change the leader key from '/' to <space>
-- ** Leader key need to be set before LazyVim **
vim.keymap.set('', '<Space>', '<Nop>', {silent = true})
vim.g.mapleader = ' '

-- Import the config files
require'config.options'
require'config.plugins'
require'config.keymaps'
require'config.styles'

-- vim: ts=2 sw=2 ft=lua expandtab:
