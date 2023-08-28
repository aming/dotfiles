#!/bin/bash

item=$1
position=$2

params=(
  script="$PLUGIN_DIR/$item.sh"
  icon.font="$FONT:Regular:19.0"
  padding_right=$PADDING
  padding_left=0
  update_freq=180
)

sketchybar --add item $item $position \
           --set $item "${params[@]}" \
           --subscribe $item power_source_change system_woke

