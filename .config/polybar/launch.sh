#!/usr/bin/env bash

# Kill running bars
killall -q polybar

# Wait until they're dead
while pgrep -u "$UID" -x polybar >/dev/null; do sleep 0.2; done

echo "---" | tee /tmp/polybar.log

# Launch main bar
polybar top -r >> /tmp/polybar.log 2>&1 &
