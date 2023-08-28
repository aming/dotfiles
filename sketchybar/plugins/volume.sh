#!/bin/sh

echo "[$NAME] Call by $SENDER with $INFO"

VOLUME=$INFO

if [[ $VOLUME == "" ]]; then
  echo "[$NAME] \$VOLUME is empty."
  exit 0
fi

VOLUME_100=􀊩
VOLUME_66=􀊧
VOLUME_33=􀊥
VOLUME_10=􀊡
VOLUME_0=􀊣

case $VOLUME in
  [6-9][0-9]|100) ICON=$VOLUME_100
    ;;
  [3-5][0-9]) ICON=$VOLUME_66
    ;;
  [1-2][0-9]) ICON=$VOLUME_33
    ;;
  [1-9]) ICON=$VOLUME_10
    ;;
  0) ICON=$VOLUME_0
    ;;
  *) ICON=$VOLUME_100
esac

sketchybar --set $NAME icon="$ICON" label="${VOLUME}%"

