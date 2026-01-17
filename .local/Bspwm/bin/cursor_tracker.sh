#!/bin/sh
#
# Cursor Tracker
# --------------
# Lightweight mouse inactivity monitor for X11.
#
# Features:
# - Enables "protection mode" after a period of mouse inactivity
# - Disables protection immediately on mouse movement
# - Locks the screen after longer inactivity
# - No sleep loops, very low CPU usage
# - Pure POSIX sh (no bash-specific features)
#
# Requirements:
# - xdotool
# - notify-send
# - X11 environment
#

# Program name (used in notifications)
program_name="Cursor Tracker"

# Time (in seconds) before protection mode is enabled
protect_time=300

# Time (in seconds) before the screen is locked
lock_time=600

# Internal state variables
counter=0
protection=0

# Screen lock command
LOCK_CMD="$HOME/.local/Bspwm/bin/screen-lock"

# Send desktop notification
notify() {
    notify-send "$program_name" "$1" -t 2000
}

# Get current mouse cursor position (X, Y)
get_cursor() {
    eval "$(xdotool getmouselocation --shell)"
}

# Initialize cursor position and timer
get_cursor
PML_X=$X
PML_Y=$Y
LAST_TIME=$(date +%s)

# Main loop
while :
do
    # Read current cursor position
    get_cursor

    # If the mouse moved, reset timers and disable protection
    if [ "$X" != "$PML_X" ] || [ "$Y" != "$PML_Y" ]; then
        counter=0

        if [ "$protection" -eq 1 ]; then
            notify "Protection disabled"
            protection=0
        fi

        PML_X=$X
        PML_Y=$Y
        LAST_TIME=$(date +%s)

    # Mouse did not move — calculate inactivity time
    else
        NOW=$(date +%s)
        counter=$((NOW - LAST_TIME))

        # Enable protection mode once inactivity threshold is reached
        if [ "$counter" -ge "$protect_time" ] && [ "$protection" -eq 0 ]; then
            notify "Protection enabled — move the mouse to disable"
            protection=1
        fi

        # Lock the screen after longer inactivity
        if [ "$counter" -ge "$lock_time" ]; then
            "$LOCK_CMD"
            counter=0
            protection=0
            LAST_TIME=$(date +%s)
        fi
    fi

    # Small non-blocking delay to keep CPU usage minimal
    read -t 0.05 < /dev/zero 2>/dev/null
done
