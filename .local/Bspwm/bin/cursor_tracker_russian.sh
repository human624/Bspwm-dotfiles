#!/bin/bash

# CONFIGURATION
program_name="Отслеживание курсора"
protect_time=150     # время до включения режима защиты
lock_time=300       # время до блокировки
counter=0           # счетчик секунд бездействия
protection=0        # статус режима защиты

# Проверка наличия xdotool
command -v xdotool >/dev/null 2>&1 || { echo >&2 "xdotool required. Install it first."; exit 1; }

get_cursor_location() {
    eval $(xdotool getmouselocation -s)
}

notify() {
    notify-send "$program_name" "$1" -t ${2:-2000} --icon="${3:-security-high}"
}

# Инициализация координат
X=0
Y=0
PML_X=0
PML_Y=0

while :; do
    sleep 1
    get_cursor_location

    if (( X != PML_X || Y != PML_Y )); then
        # мышь двигалась → сброс счетчика и режима защиты
        counter=0
        if (( protection == 1 )); then
            notify "Режим защиты выключен"
            protection=0
        fi
        PML_X=$X
        PML_Y=$Y
    else
        ((counter++))
        if (( counter == protect_time )); then
            notify "Режим защиты включен — передвиньте мышь для отключения Режима Защиты"
            protection=1
        fi

        if (( counter >= lock_time )); then
            notify "Экран заблокирован после $lock_time секунд бездействия"
            $HOME/.local/Bspwm/bin/screen-lock
            counter=0  # сброс после разблокировки
            protection=0
        fi
    fi
done
