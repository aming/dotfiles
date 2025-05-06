--------------------
-- Getting you where you want with the fewest keystrokes
-- https://github.com/ThePrimeagen/harpoon/tree/harpoon2
--------------------
return {
  {
    'ThePrimeagen/harpoon',
    branch = 'harpoon2',
    lazy = true,
    dependencies = {
      'nvim-lua/plenary.nvim'
    },
    config = function()
      require("harpoon").setup({})
    end
  },
}
