local function plugins(use)
  local opts = { noremap=true, silent=true }

  --------------------
  -- Colorscheme
  --------------------
  use { "sainnhe/gruvbox-material" }

  --------------------
  -- Status Line
  --------------------
  use {
    'nvim-lualine/lualine.nvim',
    requires = { 'kyazdani42/nvim-web-devicons', opt = true }
  }

  --------------------
  -- Neo Tree
  --------------------
  vim.g.neo_tree_remove_legacy_commands = 1 -- Unless you are still migrating, remove deprecated commands from v1.x
  use {
  "nvim-neo-tree/neo-tree.nvim",
    branch = "v2.x",
    requires = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      { "kyazdani42/nvim-web-devicons", opt = true }, -- not strictly required, but recommended
    }
  }
  vim.keymap.set('n', '<leader>n', '<cmd>Neotree toggle left<cr>', opts)
  require("neo-tree").setup({
    close_if_last_window = true,
  })

  --------------------
  -- Telescope
  --------------------
  use {
    'nvim-telescope/telescope.nvim', tag = '0.1.0',
    requires = { {'nvim-lua/plenary.nvim'} }
  }
  vim.keymap.set('n', '<C-p>', '<cmd>Telescope find_files<cr>', opts)
  vim.keymap.set('n', '<C-g>', '<cmd>Telescope live_grep<cr>', opts)
  vim.keymap.set('n', '<leader>fb', '<cmd>Telescope buffers<cr>', opts)
  vim.keymap.set('n', '<leader>fc', '<cmd>Telescope quickfix<cr>', opts)
  vim.keymap.set('n', '<leader>fgb', '<cmd>Telescope git_branches<cr>', opts)
  vim.keymap.set('n', '<leader>fgc', '<cmd>Telescope git_commits<cr>', opts)
  vim.keymap.set('n', '<leader>fgs', '<cmd>Telescope git_stash<cr>', opts)
  vim.keymap.set('n', '<leader>fh', '<cmd>Telescope help_tags<cr>', opts)
  vim.keymap.set('n', '<leader>fj', '<cmd>Telescope jumplist<cr>', opts)
  vim.keymap.set('n', '<leader>fm', '<cmd>Telescope marks<cr>', opts)
  vim.keymap.set('n', '<leader>fr', '<cmd>Telescope resume<cr>', opts)
  vim.keymap.set('n', '<leader>fs', '<cmd>Telescope search_history<cr>', opts)
  vim.keymap.set('n', '<leader>ft', '<cmd>Telescope treesitter<cr>', opts)

  --------------------
  -- LSP and Treesitter
  --------------------
  -- use 'nvim-treesitter/nvim-treesitter'
  use 'neovim/nvim-lspconfig'           -- Collection of configurations for built-in LSP client
  vim.keymap.set('n', '<space>e', vim.diagnostic.open_float, opts)
  vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
  vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
  vim.keymap.set('n', '<space>q', vim.diagnostic.setloclist, opts)

  use 'hrsh7th/nvim-cmp'                -- Autocompletion plugin
  use 'hrsh7th/cmp-nvim-lsp'            -- LSP source for nvim-cmp
  local cmp = require('cmp')
  if cmp ~= nil then
    cmp.setup({
      mapping = cmp.mapping.preset.insert({
        ['<C-d>'] = cmp.mapping.scroll_docs(-4),
        ['<C-f>'] = cmp.mapping.scroll_docs(4),
        ['<C-Space>'] = cmp.mapping.complete(),
        ['<C-e>'] = cmp.mapping.abort(),
        ['<CR>'] = cmp.mapping.confirm { select = true },
        ['<Tab>'] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_next_item()
          else
            fallback()
          end
        end, { 'i', 's' }),
        ['<S-Tab>'] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_prev_item()
          else
            fallback()
          end
        end, { 'i', 's' }),
      }),
      sources = {{ name = 'nvim_lsp' }},
    })
  else
    print 'Not able to load cmp module. Skip Autocompletion function.'
  end

  -- Use an on_attach function to only map the following keys
  -- after the language server attaches to the current buffer
  local on_attach = function(_, bufnr)
    -- Enable completion triggered by <c-x><c-o>
    vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')

    -- Mappings. See `:help vim.lsp.*` for documentation on any of the below functions
    local bufopts = { noremap=true, silent=true, buffer=bufnr }
    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, bufopts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, bufopts)
    vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, bufopts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, bufopts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, bufopts)
    vim.keymap.set('n', '<C-k>', vim.lsp.buf.signature_help, bufopts)
    vim.keymap.set('n', '<space>wa', vim.lsp.buf.add_workspace_folder, bufopts)
    vim.keymap.set('n', '<space>wr', vim.lsp.buf.remove_workspace_folder, bufopts)
    vim.keymap.set('n', '<space>wl', function()
      print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
    end, bufopts)
    vim.keymap.set('n', '<space>D', vim.lsp.buf.type_definition, bufopts)
    vim.keymap.set('n', '<space>rn', vim.lsp.buf.rename, bufopts)
    vim.keymap.set('n', '<space>ca', vim.lsp.buf.code_action, bufopts)
    vim.keymap.set('n', '<space>f', vim.lsp.buf.formatting, bufopts)
  end

  -- LSP setup
  require('lspconfig').pyright.setup {
    on_attach = on_attach,
  }

  require('lspconfig').jdtls.setup {
    on_attach = on_attach,
  }

  require'lspconfig'.gopls.setup {
    on_attach = on_attach,
  }

  require('lspconfig').sumneko_lua.setup {
    on_attach = on_attach,
    settings = {
      Lua = {
        runtime = {
          -- Tell the language server which version of Lua you're using (most likely LuaJIT in the case of Neovim)
          version = 'LuaJIT',
        },
        diagnostics = {
          -- Get the language server to recognize the `vim` global
          globals = {'vim'},
        },
        workspace = {
          -- Make the server aware of Neovim runtime files
          library = vim.api.nvim_get_runtime_file("", true),
        },
        -- Do not send telemetry data containing a randomized but unique identifier
        telemetry = {
          enable = false,
        },
      },
    },
  }

  --------------------
  -- plugins from tpope
  --------------------
  use 'tpope/vim-speeddating'
  use 'tpope/vim-surround'
  use 'tpope/vim-unimpaired'
  use 'tpope/vim-commentary'
  use 'tpope/vim-repeat'
  use 'tpope/vim-endwise'

  --------------------
  -- BeanCount
  --------------------
  use 'nathangrigg/vim-beancount'

  print("Plugins are loaded from "..vim.fn.stdpath('data'))
end

return require("packer").startup(plugins)

-- vim: ts=2 sw=2 ft=lua expandtab:
