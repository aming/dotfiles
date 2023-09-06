#!/bin/bash

item=$1
position=$2

# Yabai Icons
YABAI_STACK=􀏭
YABAI_FULLSCREEN_ZOOM=􀏜
YABAI_PARENT_ZOOM=􀥃
YABAI_FLOAT=􀢌
YABAI_GRID=􀧍

params=(
  script="$PLUGIN_DIR/$item.sh"
  icon.font="$FONT:Bold:16.0"
  label.drawing=off
  icon.width=30
  icon=$YABAI_GRID
  icon.color=$ORANGE
  padding_right=$PADDING
  padding_left=0
  associated_display=active
)

sketchybar \
  --add event window_focus \
  --add event windows_on_spaces \
  --add item $item $position \
  --set $item "${params[@]}" \
  --subscribe $item window_focus windows_on_spaces mouse.clicked

