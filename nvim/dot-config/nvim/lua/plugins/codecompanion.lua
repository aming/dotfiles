--------------------
-- CodeCompanion
-- https://github.com/olimorris/codecompanion.nvim
--------------------
return {
  {
    "olimorris/codecompanion.nvim",
    cmd = {
      "CodeCompanion",
      "CodeCompanionActions",
      "CodeCompanionChat",
      "CodeCompanionCmd",
    },
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    config = function()
      local ok, codecompanion = pcall(require, "codecompanion")
      if not ok then
        return
      end

      codecompanion.setup({
        adapters = {
          acp = {
            opencode = function()
              return require("codecompanion.adapters").extend("opencode", {
              })
            end,
          },
        },
        strategies = {
          chat = {
            adapter = "opencode",
          },
          inline = {
            adapter = "opencode",
          },
        },
        opts = {
          log_level = "ERROR",
        },
      })
    end,
  },
}
