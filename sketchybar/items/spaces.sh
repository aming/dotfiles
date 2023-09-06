#!/bin/bash

item=$1
position=$2

SPACE_ICONS=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15")

# Destroy space on right click, focus space on left click.
# New space by left clicking separator (>)

sid=0
spaces=()

for i in "${!SPACE_ICONS[@]}"
do
  sid=$(($i+1))

  space=(
    associated_space=$sid
    icon="${SPACE_ICONS[i]}"
    icon.padding_left=10
    icon.padding_right=10
    padding_left=2
    padding_right=2
    label.padding_right=20
    icon.color=$WHITE
    icon.highlight_color=$RED
    label.color=$GREY
    label.highlight_color=$WHITE
    label.font="$FONT:Regular:16.0"
    label.y_offset=-1
    background.color=$BACKGROUND_1
    background.border_color=$BACKGROUND_2
    background.drawing=off
    label.drawing=off
    script="$PLUGIN_DIR/$item.sh"
  )

  sketchybar \
    --add $item $item.$sid $position \
    --set $item.$sid "${space[@]}" \
    --subscribe $item.$sid mouse.clicked
done

spaces_bracket=(
  background.color=$BACKGROUND_1
  background.border_color=$BACKGROUND_2
  background.border_width=2
)

sketchybar \
  --add bracket spaces_bracket '/space\..*/'  \
  --set spaces_bracket "${spaces_bracket[@]}"

separator_param=(
  icon=􀆊
  icon.font="$FONT:Heavy:16.0"
  padding_left=10
  padding_right=8
  label.drawing=off
  associated_display=active
  click_script='yabai -m space --create && sketchybar --trigger space_change'
  icon.color=$WHITE
)

sketchybar \
  --add item separator $position \
  --set separator "${separator_param[@]}"

