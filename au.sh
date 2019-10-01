#!/usr/bin/env bash
# update and refresh the py3status arch-updates module

# Just in case - warn if battery level < threshold
l=$(acpi | awk -F ',' '{print $2}')
if [[ ! -z "$l" ]]; then
    level=${l:1:-1}
    threshold=40
    if [[ "$level" -lt "$threshold" ]]; then
	    echo -e "\n*** BATTERY LEVEL$l, CONNECT AC! ***\n"
    fi
fi

trizen -Syu &&
echo Press enter to exit; read; py3-cmd refresh arch_updates;
