-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  print('LazyVim not found. Bootstrap LazyVim at ' .. lazypath)
  local lazyrepo = 'https://github.com/folke/lazy.nvim.git'
  vim.fn.system({ 'git', 'clone', '--filter=blob:none', '--branch=stable', lazyrepo, lazypath })
end
vim.opt.rtp:prepend(lazypath)

-- Setup lazy.nvim
require('lazy').setup({
  spec = {
    -- import your plugins
    { import = 'plugins' },
  },
  -- colorscheme that will be used when installing plugins.
  install = { colorscheme = {'habamax'} },
  -- automatically check for plugin updates
  checker = { enabled = true },
})

-- vim: ts=2 sw=2 ft=lua expandtab:
