--------------------
-- Quarto Neovim plugin
-- https://github.com/quarto-dev/quarto-nvim
-- Need Quarto installed to work: brew install quarto
--------------------
return {
  "quarto-dev/quarto-nvim",
  dependencies = {
    "jmbuhr/otter.nvim",
    "nvim-treesitter/nvim-treesitter",
  },
  ft = {
    'quarto'
  },
  cmd = { 'Quarto' },
}
