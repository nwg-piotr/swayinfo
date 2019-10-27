#!/bin/sh
# Slightly modified example from
# https://github.com/Robinhuett/dotfiles/blob/master/.config/waybar/modules/spotify.sh

pname=$(playerctl metadata --format '{{ playerName }}')
class=$(playerctl metadata --format '{{ lc(status) }}')

if [[ $class == "playing" ]]; then
  info=$(playerctl metadata --format '{{artist}} - {{title}}')
  if [[ ${#info} > 40 ]]; then
    info=$(echo $info | cut -c1-40)"..."
  fi
  text=$pname": "$info"  "
elif [[ $class == "paused" ]]; then
  info=$(playerctl metadata --format '{{artist}} - {{title}}')
  if [[ ${#info} > 40 ]]; then
    info=$(echo $info | cut -c1-40)"..."
  fi
  text=$pname": "$info"  "
elif [[ $class == "stopped" ]]; then
  text=$pname": "
fi

echo -e "{\"text\":\""$text"\", \"class\":\""$class"\"}"
