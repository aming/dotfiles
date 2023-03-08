-- Shorten function name
local opts = { noremap = true, silent = true }

-- Change the leader key from '/' to <space>
vim.keymap.set("", "<Space>", "<Nop>", opts)
vim.g.mapleader = " "


-- Normal (n) --
-- Better window navigation
vim.keymap.set("n", "<C-h>", "<C-w>h", opts)
vim.keymap.set("n", "<C-j>", "<C-w>j", opts)
vim.keymap.set("n", "<C-k>", "<C-w>k", opts)
vim.keymap.set("n", "<C-l>", "<C-w>l", opts)
-- Navigate buffers
vim.keymap.set("n", "<S-l>", ":bnext<CR>", opts)
vim.keymap.set("n", "<S-h>", ":bprevious<CR>", opts)
-- Diagnostic Shortcuts
vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, opts)
vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, opts)
vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
-- Terminal
vim.keymap.set('n', '<leader>tt', '<cmd>ToggleTerm<cr>', opts)
-- Tree navigation
vim.keymap.set('n', '<leader>n', '<cmd>Neotree toggle left<CR>', opts)
vim.keymap.set('n', '\\', '<cmd>Neotree float reveal<CR>', opts)
-- Telescope Shortcuts
vim.keymap.set('n', '<C-p>', '<cmd>Telescope find_files<cr>', opts)
vim.keymap.set('n', '<C-g>', '<cmd>Telescope live_grep<cr>', opts)
vim.keymap.set('n', '<leader>fb', '<cmd>Telescope buffers<cr>', opts)
vim.keymap.set('n', '<leader>fc', '<cmd>Telescope quickfix<cr>', opts)
vim.keymap.set('n', '<leader>fgb', '<cmd>Telescope git_branches<cr>', opts)
vim.keymap.set('n', '<leader>fgc', '<cmd>Telescope git_commits<cr>', opts)
vim.keymap.set('n', '<leader>fgs', '<cmd>Telescope git_stash<cr>', opts)
vim.keymap.set('n', '<leader>fh', '<cmd>Telescope help_tags<cr>', opts)
vim.keymap.set('n', '<leader>fj', '<cmd>Telescope jumplist<cr>', opts)
vim.keymap.set('n', '<leader>fm', '<cmd>Telescope marks<cr>', opts)
vim.keymap.set('n', '<leader>fr', '<cmd>Telescope resume<cr>', opts)
vim.keymap.set('n', '<leader>fs', '<cmd>Telescope search_history<cr>', opts)
vim.keymap.set('n', '<leader>ft', '<cmd>Telescope treesitter<cr>', opts)
vim.keymap.set('n', '<leader>f\\', '<cmd>Telescope file_browser<cr>', opts)


-- Insert (i) --


-- Visual (v) --


-- Visual Block (x) --


-- Terminal (t) --
vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
vim.keymap.set('t', '<C-w>', [[<C-\><C-n><C-w>]], opts)


-- Command (c) --


-- vim: ts=2 sw=2 ft=lua expandtab:
