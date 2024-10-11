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
      'nvim-tree/nvim-web-devicons',
    },
    cmd = { 'Neotree' },
  },
}
