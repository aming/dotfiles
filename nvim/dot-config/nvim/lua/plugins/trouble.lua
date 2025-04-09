--------------------
-- Trouble
-- https://github.com/folke/trouble.nvim
--------------------
return {
  {
    'folke/trouble.nvim',
    cmd = "Trouble",
    opts = {
      group = true, -- group results by file
      padding = true, -- add an extra new line on top of the list
      mode = "workspace_diagnostics", -- "workspace_diagnostics", "document_diagnostics", "quickfix", "lsp_references", "loclist"
      auto_preview = true, -- automatically preview the location of the diagnostic. <esc> to close preview and go back to last window
      auto_jump = {"lsp_definitions"}, -- for the given modes, automatically jump if there is only a single result
    },
  },
}
