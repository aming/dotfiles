---------------------
--- nvim-adier
--- https://github.com/GeorgesAlkhouri/nvim-aider
---------------------
return {
  {
    "GeorgesAlkhouri/nvim-aider",
    cmd = "Aider",
    lazy = true,
    config = true,
    opts = {
      aider_cmd = 'ocaider',
        args = {
        "--no-auto-commits",
        "--pretty",
        "--watch-files",
      },
    },
    keys = {
      { "<leader>a/", "<cmd>Aider toggle<cr>", desc = "Toggle Ocaider" },
      { "<leader>as", "<cmd>Aider send<cr>", desc = "Send to Ocaider", mode = { "n", "v" } },
      { "<leader>ac", "<cmd>Aider command<cr>", desc = "Ocaider Commands" },
      { "<leader>ab", "<cmd>Aider buffer<cr>", desc = "Send Buffer" },
      { "<leader>a+", "<cmd>Aider add<cr>", desc = "Add File" },
      { "<leader>a-", "<cmd>Aider drop<cr>", desc = "Drop File" },
      { "<leader>ar", "<cmd>Aider add readonly<cr>", desc = "Add Read-Only" },
      { "<leader>aR", "<cmd>Aider reset<cr>", desc = "Reset Session" },
      { "<leader>a+", "<cmd>AiderTreeAddFile<cr>", desc = "Add File from Tree to Ocaider", ft = "neo-tree" },
      { "<leader>a-", "<cmd>AiderTreeDropFile<cr>", desc = "Drop File from Tree from Ocaider", ft = "neo-tree" },
    },
    dependencies = {
      "folke/snacks.nvim",
      "catppuccin/nvim",
      "nvim-neo-tree/neo-tree.nvim",
    },
  }
}
