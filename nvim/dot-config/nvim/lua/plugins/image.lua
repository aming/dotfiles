--------------------
-- Image support in NeoVim
-- https://github.com/3rd/image.nvim
-- Require imagemagick installed to be work: `brew install imagemagick`
--------------------
return {
  {
    '3rd/image.nvim',
    ft = {
      'markdown',
      'vimwiki',
    },
    lazy = true,
    config = function()
      require("image").setup({
        backend = "kitty",
        processor = "magick_rock", -- or "magick_cli"
        integrations = {
          markdown = {
            enabled = true,
            clear_in_insert_mode = false,
            download_remote_images = true,
            only_render_image_at_cursor = false,
            filetypes = { -- markdown extensions (ie. quarto) can go here
              "markdown",
              "vimwiki",
            },
          },
        },
        max_width = nil,
        max_height = nil,
        max_width_window_percentage = 90,
        max_height_window_percentage = 50,
        window_overlap_clear_enabled = false, -- toggles images when windows are overlapped
        window_overlap_clear_ft_ignore = { "cmp_menu", "cmp_docs", "" },
        editor_only_render_when_focused = false, -- auto show/hide images when the editor gains/looses focus
        tmux_show_only_in_active_window = false, -- auto show/hide images in the correct Tmux window (needs visual-activity off)
        hijack_file_patterns = { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.avif" }, -- render image files as images when opened
      })
    end
  },
}