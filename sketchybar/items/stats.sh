#!/bin/bash

item=$1
position=$2

params=(
  padding_right=$PADDING
  padding_left=0
)

sketchybar \
  --add alias "Stats,CPU" $position \
  --add alias "Stats,RAM" $position \
  --add alias "Stats,Network" $position

