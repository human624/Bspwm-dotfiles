#!/bin/bash

# CONFIGURATION
program_name="Отслеживание курсора"  # Название скрипта
wait_time=300  # Время до перехода в режим отслеживания
countdown=5  # Время до блокировки

# MOUSE LOCATION VARS
X=0
Y=0

# PREV MOUSE LOCATION VARS
PML_X=0
PML_Y=0

# STATUS
counter=0
protection=0

# FUNTIONS
installed() {
    command -v xdotool >/dev/null 2>&1 || {
        echo >&2 "$1 required. Please install it first.";
        exit 1;
    }
}
installed "xdotool"

get_cursor_location() {
    eval $(xdotool getmouselocation -s);
}

toggle_protection() {
    protection=$1
    if [ $1 -eq 1 ]; then
        notify "Режим защиты активирован." 20000 "security-high"
        printf "\t Режим защиты активирован.\n"
    else
        notify "Режим защиты отключён." 20000 "security-low"
        printf "\t Режим защиты отключён.\n"
    fi
}
notify() {
    notify-send "$program_name" "$1" -t ${2:-2000} --icon="${3:-security-high}"
}

# START
while :; do
    sleep 1
    get_cursor_location

    if (( $X != $PML_X || $Y != $PML_Y )); then
        # update "previous mouse locations"
        PML_X=$X
        PML_Y=$Y

        counter=0 # initialize counter again
        if [ $protection -eq 1 ]; then
        	notify "Сделайте действие."

            while [ $counter -ne $countdown ]; do
                ((counter++))
                get_cursor_location

                printf  "(%s/%s)\t Переместите курсор в указанную область. \n" \
                        "$counter" "$countdown"

                # the trigget to deactivate the protection mode
                # if mouse's y point is equal to zero (so it's on upper top)
                if [ $Y -eq 0 ]; then
                    toggle_protection 0
                    break
                fi
                sleep 1
            done

            # if the protection is active,
            if [ $protection -eq 1 ]; then
                printf "\t\t Это устройство заблокировано.\n"
                toggle_protection 0 # disable the protection
                $HOME/.local/Bspwm/bin/screen-lock
            fi
        fi
        # echo $X - $Y # debug
        printf "\t Положение курсора изменилось.\n"
    else
        ((counter++)) # increase counter
        printf "(%s/%s)\t Курсор не двигается. X: $X Y: $Y\n" \
             "$counter" "$wait_time"

        if [ $counter -ge $wait_time ] && [ $protection -eq 0 ]; then
            toggle_protection 1
        fi
    fi
done
