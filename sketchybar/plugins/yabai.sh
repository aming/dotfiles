#!/bin/bash

echo "[$NAME] Call by $SENDER with $INFO"

source "$CONFIG_DIR/colors.sh"

# Yabai Icons
YABAI_STACK=􀏭
YABAI_FULLSCREEN_ZOOM=􀏜
YABAI_PARENT_ZOOM=􀥃
YABAI_FLOAT=􀢌
YABAI_GRID=􀧍

window_state() {

  WINDOW=$(yabai -m query --windows --window)
  CURRENT=$(echo "$WINDOW" | jq '.["stack-index"]')
  ICON=""

  echo "[$NAME] window_state triggered. stack-index: $CURRENT."

  if [ "$(echo "$WINDOW" | jq '.["is-floating"]')" = "true" ]; then
    ICON+=$YABAI_FLOAT
    COLOR=$MAGENTA
  elif [ "$(echo "$WINDOW" | jq '.["has-fullscreen-zoom"]')" = "true" ]; then
    ICON+=$YABAI_FULLSCREEN_ZOOM
    COLOR=$GREEN
  elif [ "$(echo "$WINDOW" | jq '.["has-parent-zoom"]')" = "true" ]; then
    ICON+=$YABAI_PARENT_ZOOM
    COLOR=$BLUE
  elif [[ $STACK_INDEX -gt 0 ]]; then
    LAST_STACK_INDEX=$(yabai -m query --windows --window stack.last | jq '.["stack-index"]')
    ICON+=$YABAI_STACK
    LABEL="$(printf "[%s/%s]" "$STACK_INDEX" "$LAST_STACK_INDEX")"
    COLOR=$RED
  else
    ICON+=$YABAI_GRID
    COLOR=$YELLOW
  fi

  args=(--animate sin 10 --bar border_color=$COLOR
                         --set $NAME icon.color=$COLOR)

  [ -z "$LABEL" ] && args+=(label.width=0) \
                  || args+=(label="$LABEL" label.width=40)

  [ -z "$ICON" ] && args+=(icon.width=0) \
                 || args+=(icon="$ICON" icon.width=30)

  echo "[$NAME] args: ${args[@]}."
  sketchybar -m "${args[@]}"
}

windows_on_spaces () {
  echo "[$NAME] windows_on_spaces triggered"
  CURRENT_SPACES="$(yabai -m query --displays | jq -r '.[].spaces | @sh')"

  args=()
  while read -r line
  do
    for space in $line
    do
      icon_strip=" "
      apps=$(yabai -m query --windows --space $space | jq -r ".[].app")
      if [ "$apps" != "" ]; then
        while IFS= read -r app; do
          icon_strip+=" $($HOME/.config/sketchybar/plugins/icon_map.sh "$app")"
        done <<< "$apps"
      fi
      args+=(--set space.$space label="$icon_strip" label.drawing=on)
    done
  done <<< "$CURRENT_SPACES"

  sketchybar -m "${args[@]}"
}

mouse_clicked() {
  space=$(yabai -m query --spaces --space)
  current=$(echo "$space" | jq '.["type"]')
  ICON=()
  echo "[$NAME] mouse_clicked triggered. Toggle space layout from $current"

  if [ $current == "\"bsp\"" ]; then
    yabai -m space --layout float
    ICON+=$YABAI_FLOAT
    COLOR=$MAGENTA
  else
    yabai -m space --layout bsp
    ICON+=$YABAI_GRID
    COLOR=$YELLOW
  fi

  args=(
    --animate sin 10
    --bar border_color=$COLOR
    --set $NAME icon.color=$COLOR
  )

  [ -z "$LABEL" ] && args+=(label.width=0) \
                  || args+=(label="$LABEL" label.width=40)

  [ -z "$ICON" ] && args+=(icon.width=0) \
                 || args+=(icon="$ICON" icon.width=30)

  sketchybar -m "${args[@]}"
}

case "$SENDER" in
  "mouse.clicked") mouse_clicked
  ;;
  "forced") window_state
  ;;
  "window_focus") window_state 
  ;;
  "windows_on_spaces") windows_on_spaces
  ;;
esac
