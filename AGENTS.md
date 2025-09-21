# Repository Guidelines

## Project Structure & Module Organization
Each top-level directory represents configuration for a specific tool. `nvim/dot-config/nvim` contains the LazyVim-based setup, with Lua modules under `lua/config` for core behaviour and `lua/plugins` for plugin specs pinned by `lazy-lock.json`. Shell customisations live in `zsh/` alongside the `oh-my-zsh` and `oh-my-zsh-plugins` submodules. Terminal, tiling, and bar configs reside in `kitty/`, `tmux/`, `yabai/`, `skhd/`, and `sketchybar/`. Git templates live under `git/`. Use the directory naming patterns already in place (`dot-config`, `dot-<tool>`) so symlinks resolve cleanly.

## Build, Test, and Development Commands
Run `git submodule update --init --recursive` after cloning to fetch bundled themes and plugins. Use `stow --dotfiles nvim vim zsh` from the repo root to symlink selected toolsets into your `$HOME`. `rake install` links root-level `*rc`, `*conf`, and `*config` files, prompting before replacing existing files. After linking Neovim configs, open `nvim` and execute `:Lazy sync` to ensure plugins match `lazy-lock.json`.

## Coding Style & Naming Conventions
Stick with two-space indentation across Lua, shell, and YAML files; the editors are preconfigured for that (`init.lua` enforces `ts=2 sw=2`). Lua modules under `lua/config` should export descriptive tables and keep filenames aligned with their feature (`keymaps.lua`, `styles.lua`). For Zsh, prefer `.zsh` suffixes and keep plugin folders named after their upstream repository. When adding new binaries or assets, place them within the matching tool directory to keep Stow targets predictable.

## Testing Guidelines
There is no automated test suite; validate changes by launching the affected tool. For Neovim, run `nvim --clean -u nvim/dot-config/nvim/init.lua` to confirm new plugins load without errors. For shell changes, start a new terminal session or run `zsh -il` to exercise login scripts. Capture before/after screenshots for status-bar or window-manager tweaks when practical.

## Commit & Pull Request Guidelines
Follow the existing Git history: concise, imperative subject lines such as "Add kitty icon" or "Move shortcut keys to keymap.lua". Reference related issues directly in the body if applicable and note whether manual verification was performed. Pull requests should outline the affected tools, list any new dependencies or submodules, and attach screenshots for visual updates. Confirm `rake install` or `stow` paths if contributors need rerun steps after merging.
