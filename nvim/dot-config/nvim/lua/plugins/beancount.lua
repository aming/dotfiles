--------------------
-- BeanCount
--------------------


return {
  {
    'crispgm/cmp-beancount',
    ft = {
      "beancount",
    },
    config = function()
      -- local util = require 'lspconfig.util'
      -- local root_dir = function(fname)
      --   return util.find_git_ancestor(fname) or util.path.dirname(fname)
      -- end;
      vim.lsp.config('beancount', {
        -- init_options = {
        --   journal_file = root_dir..'/main.bean'
        -- },
      })
      vim.lsp.enable('beancount')
      vim.treesitter.start()
    end
  },
}
