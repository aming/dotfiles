#!/bin/bash

item=$1
position=$2

params=(
  script="$PLUGIN_DIR/$item.sh"
  label.font="$FONT:Regular:14.0"
  padding_right=$PADDING
  padding_left=0
  label.width=0
)

sketchybar \
  --add item $item $position \
  --set $item "${params[@]}" \
  --subscribe $item wifi_change mouse.clicked

