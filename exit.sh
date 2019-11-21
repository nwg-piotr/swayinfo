#!/usr/bin/env bash

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
    *Logout) swaynag -t warning -m 'Do you really want to exit sway?' -b 'Exit sway' 'swaymsg exit' ;;
    *Reboot) swaynag -t warning -m 'Do you really want to restart the machine?' -b 'Reboot' 'systemctl reboot' ;;
    *Shutdown) swaynag -t warning -m 'Do you really want to turn the machine off?' -b 'Shutdown' 'systemctl -i poweroff'
esac

exit 0
