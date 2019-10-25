#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import subprocess

pacman = subprocess.check_output("checkupdates", shell=True).decode("utf-8").splitlines()
aur = subprocess.check_output("trizen -Qqu -a", shell=True).decode("utf-8").splitlines()

updates = ''
if len(pacman) > 0 or len(aur) > 0:
    updates += ' {}/{}'.format(len(pacman), len(aur))

print('{"text":"%s"}' % (updates))