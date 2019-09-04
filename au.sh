#!/usr/bin/env bash
# update and refresh the py3status arch-updates module
trizen -Syu &&
echo Press enter to exit; read; py3-cmd refresh arch_updates;
