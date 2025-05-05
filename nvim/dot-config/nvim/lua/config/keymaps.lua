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
-- LSP Shortcuts
vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
vim.keymap.set("n", "<leader>lf", vim.lsp.buf.format, opts)
vim.keymap.set('n', '<leader>gd', vim.lsp.buf.definition, opts)
vim.keymap.set('n', '<leader>gr', vim.lsp.buf.references, opts)
vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
-- Telepscope Shortcuts
vim.keymap.set('n', '<C-p>', ':Telescope find_files<CR>', opts)
vim.keymap.set('n', '<C-g>', ':Telescope live_grep<CR>', opts)
vim.keymap.set('n', '<leader>t', ':Telescope<CR>', opts)
vim.keymap.set('n', '<leader>tr', ':Telescope<CR>', opts)
vim.keymap.set('n', '<leader>ts', ':Telescope grep_string<CR>', opts)
vim.keymap.set('n', '<leader>tb', ':Telescope buffers<CR>', opts)
vim.keymap.set('n', '<leader>to', ':Telescope oldfiles<CR>', opts)
vim.keymap.set('n', '<leader>tc', ':Telescope quickfix<CR>', opts)
vim.keymap.set('n', '<leader>tj', ':Telescope jumplist<CR>', opts)
vim.keymap.set('n', '<leader>th', ':Telescope help_tags<CR>', opts)
vim.keymap.set('n', '<leader>tm', ':Telescope marks<CR>', opts)
vim.keymap.set('n', '<leader>tt', ':Telescope treesitter<CR>', opts)
vim.keymap.set('n', '<leader>tk', ':Telescope keymaps<CR>', opts)


-- Insert Mode (i) --
-- Completion Shortcuts
local cmp = require("cmp")
vim.keymap.set('i', '<Tab>', cmp.mapping.complete(), opts)
vim.keymap.set('i', '<C-u>', cmp.mapping.scroll_docs(-4), opts)
vim.keymap.set('i', '<C-f>', cmp.mapping.scroll_docs(4), opts)
vim.keymap.set('i', '<C-e>', cmp.mapping.abort(), opts)
vim.keymap.set('i', '<CR>', cmp.mapping.confirm({ select = true }), opts)


-- Visual Mode (v) --


-- Terminal Mode (t) --


-- Command Mode (c) --


-- File Navigation (n) --


-- File Navigation (n) --


-- Insert (i) --


-- Visual (v) --


-- Visual Block (x) --


-- Terminal (t) --
vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
vim.keymap.set('t', '<C-w>', [[<C-\><C-n><C-w>]], opts)


-- Command (c) --


-- vim: ts=2 sw=2 ft=lua expandtab:
