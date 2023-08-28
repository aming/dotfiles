#!/bin/bash

item=cpu

params=(
  script="$PLUGIN_DIR/$item.sh"
  label.font="$FONT:Regular:14.0"
  padding_right=5
  padding_left=0
  updates=on
)

cpu_top_params=(
  label.font="$FONT:Semibold:7"
  label=CPU
  icon.drawing=off
  width=0
  padding_right=15
  y_offset=6
)

cpu_sys_params=(
  width=0
  graph.color=$RED
  graph.fill_color=$RED
  label.drawing=off
  icon.drawing=off
  background.height=30
  background.drawing=on
  background.color=$TRANSPARENT
)

cpu_user_params=(
  graph.color=$BLUE
  label.drawing=off
  icon.drawing=off
  background.height=30
  background.drawing=on
  background.color=$TRANSPARENT
)

sketchybar --add item cpu.top right              \
           --set cpu.top "${cpu_top_params[@]}"         \
                                                 \
           --add graph cpu.sys right 75          \
           --set cpu.sys "${cpu_sys_params[@]}"         \
                                                 \
           --add graph cpu.user right 75         \
           --set cpu.user "${cpu_user_params[@]}"
