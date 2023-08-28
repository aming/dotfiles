#!/usr/bin/env bash

SOURCE=$(defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleCurrentKeyboardLayoutInputSourceID)

LABEL='?'

case ${SOURCE} in
  'com.apple.keylayout.ABC') LABEL='A' ;;
  'com.apple.keylayout.Dvorak') LABEL='Dv' ;;
  'com.apple.keylayout.CangjieKeyboard') LABEL='倉' ;;
  'com.apple.keylayout.TraditionalPinyinKeyboard') LABEL='拼' ;;
esac

sketchybar --set $NAME label="$LABEL"
