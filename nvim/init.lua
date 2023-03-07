----------------------------------------
-- A neovim configuration file for AMing
-- Maintainer:	AMing (cyberming at gmail dot com)
--
-- To use it, copy or link nvim to ~/.config/nvim
----------------------------------------

-- Set the runtime path to Dotfiles directory
vim.cmd('set runtimepath=$HOME/dotfiles/nvim,$VIMRUNTIME')
vim.cmd('let packpath=&runtimepath')

require'user.keymaps'
require'user.options'
require'user.plugins'
require'user.styles'

require'lsp'

-- vim: ts=2 sw=2 ft=lua expandtab:
