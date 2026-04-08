# AEROSPACE

## OVERVIEW
Single-file AeroSpace configuration for workspace bindings, layout rules, and startup integration with SketchyBar.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| All AeroSpace behavior | `aerospace/dot-config/aerospace/aerospace.toml` | startup, gaps, bindings, service mode |

## CONVENTIONS
- This subtree is intentionally single-file; keep related bindings together instead of fragmenting them.
- `after-startup-command` currently launches `sketchybar`; changes here can affect bar behavior indirectly.
- Workspace bindings are explicit and repetitive by design; consistency matters more than clever compaction.

## ANTI-PATTERNS
- Do not change startup commands without checking SketchyBar coupling.
- Do not mix unrelated experiments into the service mode bindings; they are operational recovery commands.

## COMMANDS
```bash
# Reload from AeroSpace itself after editing the TOML.
```
