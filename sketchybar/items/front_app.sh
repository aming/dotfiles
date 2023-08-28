#!/bin/bash

item=$1
position=$2

params=(
  script="$PLUGIN_DIR/$item.sh"
  icon.drawing=off
  label.drawing=on
  label.font="$FONT:Bold:12.0"
  associated_display=active
)

sketchybar \
  --add item $item $position \
  --set $item "${params[@]}" \
  --subscribe $item front_app_switched

