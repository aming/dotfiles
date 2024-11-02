--------------------
-- Neo Tree
-- https://github.com/nvim-neo-tree/neo-tree.nvim
--------------------
return {
  {
    'nvim-neo-tree/neo-tree.nvim',
    branch = 'v3.x',
    dependencies = {
      'nvim-lua/plenary.nvim',
      'MunifTanjim/nui.nvim',
      'nvim-tree/nvim-web-devicons', -- not strictly required, but recommended
      "3rd/image.nvim", -- Optional image support in preview window
    },
    cmd = { 'Neotree' },
    config = function()
      require('neo-tree').setup({
        window = {
          mappings = {
            ["P"] = { "toggle_preview", config = { use_float = false, use_image_nvim = true } },
          },
        },
      })
    end
  },
}
