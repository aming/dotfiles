#!/bin/bash

item=$1
position=$2

params=(
  script="$PLUGIN_DIR/$item.sh"
  padding_right=$PADDING
  padding_left=0
  update_freq=60
)

sketchybar \
  --add item $item $position \
  --set $item "${params[@]}" \
  --subscribe $item system_woke mouse.clicked

