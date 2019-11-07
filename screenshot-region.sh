#!/bin/bash

sleep 5

SAVEDIR=${SWAY_INTERACTIVE_SCREENSHOT_SAVEDIR:=~/Obrazy/Screenshots}
mkdir -p -- "$SAVEDIR"
FILENAME="$SAVEDIR/$(date +'%Y-%m-%d-%H%M%S_screenshot.png')"
EXPENDED_FILENAME="${FILENAME/#\~/$HOME}"

grim -g "$(slurp)" "$EXPENDED_FILENAME"

wl-copy < "$EXPENDED_FILENAME"
notify-send "Screenshot" "File saved as <i>'$FILENAME'</i> and copied to the clipboard." -i "$EXPENDED_FILENAME"