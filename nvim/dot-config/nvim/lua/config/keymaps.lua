-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local opts = { noremap = true, silent = true }

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
-- Navigate buffers
vim.keymap.set('n', '<S-l>', ':bnext<CR>', opts)
vim.keymap.set('n', '<S-h>', ':bprevious<CR>', opts)
-- Diagnostic Shortcuts
vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, opts)
vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, opts)
vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
-- Tree navigation
vim.keymap.set('n', '<leader>n', '<cmd>Neotree toggle left<CR>', opts)
vim.keymap.set('n', '\\', '<cmd>Neotree float reveal<CR>', opts)
-- Telescope Shortcuts
vim.keymap.set('n', '<C-p>', '<cmd>Telescope find_files<cr>', opts)
vim.keymap.set('n', '<C-g>', '<cmd>Telescope live_grep<cr>', opts)
vim.keymap.set('n', '<leader>tr', '<cmd>Telescope resume<cr>', opts)
vim.keymap.set('n', '<leader>tb', '<cmd>Telescope buffers<cr>', opts)
vim.keymap.set('n', '<leader>tc', '<cmd>Telescope quickfix<cr>', opts)
vim.keymap.set('n', '<leader>tj', '<cmd>Telescope jumplist<cr>', opts)
vim.keymap.set('n', '<leader>th', '<cmd>Telescope help_tags<cr>', opts)
vim.keymap.set('n', '<leader>tm', '<cmd>Telescope marks<cr>', opts)
vim.keymap.set('n', '<leader>to', '<cmd>Telescope oldfiles<cr>', opts)
vim.keymap.set('n', '<leader>tgb', '<cmd>Telescope git_branches<cr>', opts)
vim.keymap.set('n', '<leader>tgc', '<cmd>Telescope git_commits<cr>', opts)
vim.keymap.set('n', '<leader>tgs', '<cmd>Telescope git_stash<cr>', opts)
vim.keymap.set('n', '<leader>ts', '<cmd>Telescope search_history<cr>', opts)
vim.keymap.set('n', '<leader>tt', '<cmd>Telescope treesitter<cr>', opts)
vim.keymap.set('n', '<leader>tf', '<cmd>Telescope file_browser<cr>', opts)


-- Insert (i) --


-- Visual (v) --


-- Visual Block (x) --


-- Terminal (t) --
vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
vim.keymap.set('t', '<C-w>', [[<C-\><C-n><C-w>]], opts)


-- Command (c) --


-- vim: ts=2 sw=2 ft=lua expandtab:
