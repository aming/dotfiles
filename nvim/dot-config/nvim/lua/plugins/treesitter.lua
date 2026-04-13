--------------------
-- Treesitter plugins settings
-- tree-sitter cli in required
--   apt install tree-sitter-cli / brew install tree-sitter
-- Supported langauge: https://github.com/nvim-treesitter/nvim-treesitter/blob/main/SUPPORTED_LANGUAGES.md
--------------------
return {
  {
    -- https://github.com/nvim-treesitter/nvim-treesitter
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,  -- This plugin does not support lazy-loading.
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter").setup({
        install_dir = vim.fn.stdpath("data") .. "/site",
      })
    end
  }
}
