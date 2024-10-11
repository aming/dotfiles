-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local opts = {
  noremap = true, -- Avoid mapping recursively
  silent = true,  -- No echoed on the command line
}

-- Leader key need to be set before LazyVim
-- Change the leader key from '/' to <space>
vim.keymap.set('', '<Space>', '<Nop>', opts)
vim.g.mapleader = ' '

-- Normal (n) --
-- Better window navigation
vim.keymap.set('n', '<C-h>', '<C-w>h', opts)
vim.keymap.set('n', '<C-j>', '<C-w>j', opts)
vim.keymap.set('n', '<C-k>', '<C-w>k', opts)
vim.keymap.set('n', '<C-l>', '<C-w>l', opts)
-- Diagnostic Shortcuts
vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, opts)
vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, opts)
vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
-- Tree navigation
vim.keymap.set('n', '<leader>n', '<cmd>Neotree toggle left<CR>', opts)
vim.keymap.set('n', '\\', '<cmd>Neotree float reveal<CR>', opts)
-- Telescope Shortcuts
local telescope = require('telescope.builtin')
vim.keymap.set('n', '<C-p>', telescope.find_files, opts)
vim.keymap.set('n', '<C-g>', telescope.live_grep, opts)
vim.keymap.set('n', '<leader>t', telescope.builtin, opts)
vim.keymap.set('n', '<leader>tr', telescope.resume, opts)
vim.keymap.set('n', '<leader>ts', telescope.grep_string, opts)
vim.keymap.set('n', '<leader>tb', telescope.buffers, opts)
vim.keymap.set('n', '<leader>to', telescope.oldfiles, opts)
vim.keymap.set('n', '<leader>tc', telescope.quickfix, opts)
vim.keymap.set('n', '<leader>tj', telescope.jumplist, opts)
vim.keymap.set('n', '<leader>th', telescope.help_tags, opts)
vim.keymap.set('n', '<leader>tm', telescope.marks, opts)
vim.keymap.set('n', '<leader>tt', telescope.treesitter, opts)
vim.keymap.set('n', '<leader>tk', telescope.keymaps, opts)


-- Insert (i) --


-- Visual (v) --


-- Visual Block (x) --


-- Terminal (t) --
vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
vim.keymap.set('t', '<C-w>', [[<C-\><C-n><C-w>]], opts)


-- Command (c) --


-- vim: ts=2 sw=2 ft=lua expandtab:
