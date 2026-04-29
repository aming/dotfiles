# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-08
**Commit:** `4c7b0c7`
**Branch:** `master`

## OVERVIEW
Personal macOS dotfiles managed with GNU Stow. Most top-level directories map to one tool; large `zsh/`, `vim/`, and `tmux/dot-tmux/plugins/tpm` trees are mostly vendored or submodule-managed, not day-to-day authoring surfaces.

## STRUCTURE
```text
dotfiles/
├── aerospace/   # AeroSpace window manager config
├── agents/      # OpenCode skills, helper scripts
├── docs/        # plans and retained project notes
├── nvim/        # Neovim config, Lazy specs, lockfile
├── opencode/    # OpenCode/OCX profiles
├── sketchybar/  # bar entrypoint plus item/plugin scripts
├── tmux/        # tmux.conf; TPM below here is vendored
├── vim/         # mostly checked-in plugin content
└── zsh/         # shell config plus oh-my-zsh submodules
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Bootstrap a machine | `README.md` | clone, submodules, brew, stow |
| Update submodules | `.gitmodules` | authoritative vendor list |
| Neovim startup | `nvim/dot-config/nvim/init.lua` | imports `config.*` modules |
| Neovim plugin wiring | `nvim/dot-config/nvim/lua/plugins/` | one file per plugin area |
| SketchyBar entrypoint | `sketchybar/sketchybarrc` | sources `items/` and shared palette |
| SketchyBar shared theme | `sketchybar/colors.sh`, `sketchybar/icons.sh` | central constants |
| AeroSpace bindings | `aerospace/dot-config/aerospace/aerospace.toml` | launches `sketchybar` on startup |
| tmux entrypoint | `tmux/dot-tmux.conf` | TPM loaded at end |
| OpenCode profiles | `opencode/dot-config/opencode/profiles/` | `default/` and `omo/` diverge |
| Agent skills and utilities | `agents/dot-agents/skills/` | first-party skill definitions |
| Agent learnings | `.agent/learnings/ERRORS.md` | environment-specific failures |
| Project plans | `docs/superpowers/plans/` | change plans and retained notes |

## CODE MAP
LSP workspace symbol scan was not usable at repo-root granularity here. Treat the top-level domains above as the practical map; the maintained code lives mostly in `agents/`, `nvim/`, `sketchybar/`, `opencode/`, and `aerospace/`.

## CONVENTIONS
- Top-level directories are tool-scoped. `dot-config` mirrors `~/.config`; `dot-<name>` mirrors other dotfile targets.
- Bootstrap path is stable: `git submodule update --init --recursive`, install toolchain, then `stow --dotfiles <tool...>`.
- Neovim config uses two-space indentation and `expandtab`; many Lua files carry `vim: ts=2 sw=2 ft=lua expandtab` modelines.
- Neovim plugins are declared as separate specs under `nvim/dot-config/nvim/lua/plugins/`; pinned state lives in `nvim/dot-config/nvim/lazy-lock.json`.
- SketchyBar uses one entry script plus shared `colors.sh` / `icons.sh`, with per-item wrappers under `items/` and behavior under `plugins/`.
- OpenCode profiles keep `opencode.jsonc` for model/plugin config and `ocx.jsonc` for include/exclude behavior.

## ANTI-PATTERNS (THIS PROJECT)
- Do not treat `vim/plugged`, `zsh/oh-my-zsh`, `zsh/oh-my-zsh-plugins`, or `tmux/dot-tmux/plugins/tpm` as first-party refactor targets unless the task is explicitly a dependency/submodule update.
- Do not add plugin/theme code directly inside vendored submodule trees when the repo already has first-party config surfaces around them.
- Do not use deprecated Neovim LSP setup patterns like `require('lspconfig').<server>.setup(...)`; ongoing notes point toward the Neovim 0.11 API.
- Do not forget submodule bookkeeping when adding/removing shell plugins; `README.md` assumes git submodule workflows.
- Do not rely on the placeholder `opencode` profile AGENTS content; this file set replaces it with repo-specific guidance.

## UNIQUE STYLES
- This repo keeps operational docs in-repo under `docs/`, especially `docs/superpowers/plans/*` for change plans and retained context.
- `agents/` is not generic docs; it is a working skill library with scripts, eval artifacts, and environment learnings.
- `aerospace` and `sketchybar` are coupled: AeroSpace startup launches SketchyBar, and bar plugins expect macOS command availability.

## COMMANDS
```bash
git submodule update --init --recursive
stow --dotfiles nvim vim zsh
stow -D nvim vim zsh
nvim --clean -u nvim/dot-config/nvim/init.lua
# In Neovim: :Lazy sync
zsh -il
```

## NOTES
- `README.md` references this root file. Keep it current when repository shape or bootstrap steps change.
- Formal tests mostly belong to vendored/plugin subtrees. First-party verification is primarily manual: start the tool, sync plugins, or run the relevant helper script.
- `tmux/` and `zsh/` look large only because submodules and embedded plugin assets dominate file count.
