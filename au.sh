#!/usr/bin/env bash
# update and refresh the py3status arch-updates module

# Just in case - warn if battery level < threshold
l=$(acpi | awk -F ',' '{print $2}')
level=${l:1:-1}
threshold=40
if [[ "$level" -lt "$threshold" ]]; then
	echo "Battery level$l, connect AC!"
fi

trizen -Syu &&
echo Press enter to exit; read; py3-cmd refresh arch_updates;
