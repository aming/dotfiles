#!/bin/bash

item=$1
position=$2

params=(
  script="$PLUGIN_DIR/$item.sh"
  padding_right=$PADDING
  padding_left=0
)

sketchybar \
  --add event input_change 'AppleSelectedInputSourcesChangedNotification' \
  --add item $item $position \
  --set $item "${params[@]}" \
  --subscribe $item input_change

