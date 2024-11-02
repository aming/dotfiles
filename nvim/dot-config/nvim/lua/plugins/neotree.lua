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
    keys = {
      { '\\', ':Neotree reveal<CR>', { desc = 'Reveal the current file in NeoTree' } },
      { '<leader>n', ':Neotree toggle left<CR>' },
    },
    opts = {
      close_if_last_window = true, -- Close Neo-tree if it is the last window left in the tab
      enable_git_status = true,
      enable_diagnostics = true,
      open_files_do_not_replace_types = { "terminal", "trouble", "qf" }, -- when opening files, do not use windows containing these filetypes or buftypes
      filesystem = {
        hijack_netrw_behavior = 'open_default', -- open a directory in neo-tree
        use_libuv_file_watcher = true,  -- use the OS level file watchers to detect changes
      },
      window = {
        mappings = {
          ['P'] = {
            'toggle_preview',
            config = {
              use_float = true,
              use_image_nvim = true,
            },
          },
        },
      },
    },
  },
}
