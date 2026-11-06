-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
-- List current monitors and supported resolutions with: hyprctl monitors all

-- Monitor scale is Hyprland's scale for the output. It sizes everything
-- Wayland-native, accepts fractions (1.6, 1.75), and applies immediately.
-- "auto" lets Hyprland pick per display.
local omarchy_monitor_scale = "auto"
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })

-- Configure a specific monitor.
-- The Dell U3417W is matched by EDID description, not by output name: i915
-- enumerates the same panel as DP-4 on some boots and DP-5 on others (both
-- connectors exist; they are separate DDI/AUX channels), so a name-keyed rule
-- silently misses and the `output = ""` rule above auto-places the display.
-- `desc:` is a prefix match on `hyprctl monitors`' description field.
-- Above the Samsung: 3440x1440 at scale 1 is 3440x1440 in layout px, centred
-- over the Samsung's 5120 layout width -> x = (5120 - 3440) / 2 = 840.
-- `omarchy_monitor_scale` is "auto", which resolves to 1 on both panels here;
-- if either ever resolves higher, 840/1440 stop aligning and must be redone
-- from the scaled sizes (see `hyprctl monitors`).
-- y = 0 and height 1440 make its bottom edge meet the Samsung's top edge
-- (y = 1440) exactly; any gap leaves the two outputs non-adjacent, and the
-- cursor then cannot cross between them.
hl.monitor({ output = "desc:Dell Inc. DELL U3417W", mode = "3440x1440@60", position = "840x0", scale = omarchy_monitor_scale })
-- Samsung Odyssey G91F (LS49FG201ENXZA): matched by EDID description for the
-- same reason as the Dell — connector names are per i915 DDI, not per panel.
-- 5120x1440 is the native panel mode. It only works with AQ_NO_MODIFIERS=1 in
-- ~/.config/uwsm/env, because i915 on Comet Lake rejects Y-tiled framebuffers
-- wider than 4096 px. 5120x1440@120/144 exceed the 675 MHz max dotclock of
-- Gen9.5 and cannot be used.
hl.monitor({ output = "desc:Samsung Electric Company Odyssey G91F", mode = "5120x1440@60", position = "0x1440", scale = omarchy_monitor_scale })

-- Portrait/rotated secondary monitor (transform: 1 = 90°, 3 = 270°).
-- hl.monitor({ output = "desc:Samsung Electric Company Odyssey G91F", mode = "preferred", position = "auto", scale = 1, transform = 1 })

-- GDK scale is GDK_SCALE, the factor GTK draws its own UI at. It's what
-- sizes X11/XWayland windows, which Omarchy leaves unscaled so they stay
-- crisp instead of being stretched by the compositor. GTK only honors whole
-- numbers, so use the nearest integer to the monitor scale, and restart an
-- app for a change to reach it.
local omarchy_gdk_scale = 1
hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))
