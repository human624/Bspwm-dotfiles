#!/usr/bin/env bash

killall -q polybar
# Пока polybar закрывается, мы не ждем вечно
while pgrep -u "$UID" -x polybar >/dev/null; do sleep 0.1; done

# Если один монитор, запустится один раз. Если подключишь второй — на обоих.
if type "xrandr" > /dev/null; then
  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m polybar top -r &
  done
else
  polybar top -r &
fi
