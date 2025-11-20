return {
  {
    "akinsho/toggleterm.nvim",
    version = "*",
    config = function()
      require("toggleterm").setup({
        direction = "horizontal",
        size = 20,
        start_in_insert = true,
      })

      -- Create a dedicated Aider Watch terminal
      local Terminal = require("toggleterm.terminal").Terminal
      AiderWatch = Terminal:new({
        cmd = "aider --watch-files",
        direction = "horizontal",
        close_on_exit = false,
        hidden = true,
      })
      function _AIDER_WATCH_TOGGLE()
        AiderWatch:toggle()
      end
    end,
    keys = {
      { "<leader>aw", "<cmd>lua _AIDER_WATCH_TOGGLE()<CR>", desc = "Toggle Aider Watch Mode" },
    },
  },
}

