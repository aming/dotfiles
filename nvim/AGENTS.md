# NVIM

## OVERVIEW
Neovim 0.11+ configuration built around `lazy.nvim` with local config modules and separate plugin specs.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Startup path | `nvim/dot-config/nvim/init.lua` | sets runtimepath, leader, imports config |
| Core options | `nvim/dot-config/nvim/lua/config/options.lua` | editing defaults, filetypes |
| Plugin bootstrap | `nvim/dot-config/nvim/lua/config/plugins.lua` | bootstraps `lazy.nvim` |
| Keymaps and styling | `nvim/dot-config/nvim/lua/config/keymaps.lua`, `styles.lua` | local behavior |
| Feature/plugin changes | `nvim/dot-config/nvim/lua/plugins/*.lua` | one focused spec file per area |
| Locked versions | `nvim/dot-config/nvim/lazy-lock.json` | update when plugin set changes |

## CONVENTIONS
- Two-space indentation and `expandtab` are explicit here.
- Keep `init.lua` thin; put behavior in `lua/config/*` or a dedicated plugin spec.
- Add plugin changes as separate files under `lua/plugins/` when they represent a distinct area.
- `config/plugins.lua` bootstraps `lazy.nvim`; do not move that logic into random plugin files.
- This config errors on Neovim versions older than 0.11.

## ANTI-PATTERNS
- Do not reintroduce deprecated `require('lspconfig').<server>.setup(...)` patterns.
- Do not hand-edit lock state casually; if plugin intent changes, verify `lazy-lock.json` stays in sync.
- Do not put unrelated keymaps, options, and plugin specs into the same file just because the edit is small.

## COMMANDS
```bash
nvim --clean -u nvim/dot-config/nvim/init.lua
# In Neovim: :Lazy sync
```

## NOTES
- `options.lua` registers `*.bean` as `beancount`; keep filetype additions close to options.
- `config/plugins.lua` enables Lazy's update checker, so startup behavior may surface plugin drift.
