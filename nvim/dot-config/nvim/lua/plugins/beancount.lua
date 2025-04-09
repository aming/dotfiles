--------------------
-- BeanCount
--------------------


return {
  {
    'crispgm/cmp-beancount',
    ft = {
      "beancount",
      "bean",
    },
    config = function()
      local lspconfig = require('lspconfig')
      -- local util = require 'lspconfig.util'
      -- local root_dir = function(fname)
      --   return util.find_git_ancestor(fname) or util.path.dirname(fname)
      -- end;
      lspconfig.beancount.setup({
        -- init_options = {
        --   journal_file = root_dir..'/main.bean'
        -- },
      })
    end
  },
}

