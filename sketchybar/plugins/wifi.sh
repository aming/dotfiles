#!/bin/sh

# The wifi_change event supplies a $INFO variable in which the current SSID
# is passed to the script.


WIFI_CONNECTED=􀙇
WIFI_DISCONNECTED=􀙈

update() {
  echo "[Wifi] Update with $INFO"
  LABEL="$INFO ($(ipconfig getifaddr en0))"
  ICON="$([ -n "$INFO" ] && echo "$WIFI_CONNECTED" || echo "$WIFI_DISCONNECTED")"
  sketchybar --set $NAME icon="$ICON" label="$LABEL"
}


click() {
  echo "[Wifi] Click with $INFO"
  CURRENT_WIDTH="$(sketchybar --query $NAME | jq -r .label.width)"

  WIDTH=0
  if [ "$CURRENT_WIDTH" -eq "0" ]; then
    WIDTH=dynamic
  fi

  sketchybar --animate sin 20 --set $NAME label.width="$WIDTH"
}


case "$SENDER" in
  "wifi_change") update
    ;;
  "mouse.clicked") click
    ;;
esac
