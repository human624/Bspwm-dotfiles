#!/bin/bash

CURRENT_LAYOUT=$(xset -q | grep LED | awk '{ print $10 }')

setxkbmap -layout us,ru -option "grp:alt_shift_toggle,ctrl:nocaps"

case "$CURRENT_LAYOUT" in
    "00000000") notify-send "Lang: US" -t 700 ;;
    "00001000") notify-send "Lang: RU" -t 700 ;;
esac
