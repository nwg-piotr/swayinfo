#!/usr/bin/env bash

# A rofi-like System/Exit menu for wofi

# wofi crashes w/ no cache file, so let's use a custom one and delete it every time, to avoid reordering entries
rm /home/piotr/.local/share/wofi/exit.cache

A=$(wofi --show dmenu --width=100 --height=110 --cache-file=/home/piotr/.local/share/wofi/exit.cache --prompt=System cat <<EOF
 Lock
 Logout
 Reboot
 Shutdown
EOF
)

case "$A" in

    *Lock) swaylock -f -c 000000 ;;

    *Logout) swaynagmode -R -t red -m ' You are about to exit Sway. Proceed?' \
      -b '  Logout ' 'swaymsg exit' \
      -b '  Reload ' 'swaymsg reload' ;;

    *Reboot) swaynagmode -R -t red -m ' You are about to restart the machine? Proceed?' \
      -b '  Reboot ' 'systemctl reboot' ;;

    *Shutdown) swaynagmode -R -t red -m ' You are about to turn the machine off. Proceed?' \
      -b '  Shutdown ' 'systemctl -i poweroff' ;;

esac

exit 0