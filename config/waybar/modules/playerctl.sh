#!/bin/sh
# based on https://github.com/Robinhuett/dotfiles/blob/master/.config/waybar/modules/spotify.sh

pname=$(playerctl metadata --format '{{ playerName }}')
class=$(playerctl metadata --format '{{ lc(status) }}')

if [[ ${class} == "playing" ]] || [[ ${class} == "paused" ]]; then
  info=$(playerctl metadata --format '{{artist}} - {{title}}')
  if [[ ${#info} > 60 ]]; then
    info=$(echo ${info} | cut -c1-60)"..."
  fi
fi

if [[ ${class} == "playing" ]]; then
  text=${pname}": "${info}"  "
elif [[ ${class} == "paused" ]]; then
  text=${pname}": "${info}"  "
elif [[ $class == "stopped" ]]; then
  text=${pname}": "
fi

echo -e "{\"text\":\""${text}"\", \"class\":\""${class}"\"}"
