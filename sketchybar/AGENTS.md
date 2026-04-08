# SKETCHYBAR

## OVERVIEW
SketchyBar config with one entrypoint, shared palette/icon files, and split item/plugin scripts.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Main bar wiring | `sketchybar/sketchybarrc` | sources colors and item scripts |
| Shared palette | `sketchybar/colors.sh` | bar and popup colors |
| Shared icons | `sketchybar/icons.sh` | central icon constants |
| Item declarations | `sketchybar/items/*.sh` | adds items, aliases, positions |
| Runtime behavior | `sketchybar/plugins/*.sh` | event handlers, system queries |
| Toggle logic | `sketchybar/plugins/toggle_stats.sh` | stateful item visibility |

## CONVENTIONS
- `sketchybarrc` is the only top-level entrypoint; keep it as orchestration, not heavy logic.
- Shared visual constants belong in `colors.sh` and `icons.sh`.
- `items/` scripts define bar items and subscribe them; `plugins/` scripts do the work.
- Scripts assume macOS utilities like `pmset`, `osascript`, `jq`, `df`, and SketchyBar itself are available.

## ANTI-PATTERNS
- Do not duplicate color or icon literals across plugins when shared files already exist.
- Do not put first-run `sketchybar --update` calls inside item/plugin scripts; `sketchybarrc` already owns that.
- Do not ignore coupling with AeroSpace/Yabai plugins when changing workspace or front-app behavior.

## COMMANDS
```bash
sketchybar --update
```

## NOTES
- `sketchybarrc` currently launches left, notch-adjacent, and right-side groups explicitly; preserve that mental model when adding items.
- `toggle_stats.sh` uses `separator_right` icon state as its toggle source of truth.
