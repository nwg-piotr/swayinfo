#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script displays a notification when battery is low or full

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Website: http://nwg.pl
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Dependencies: upower, obhud (AUR)
"""

import sys
import subprocess


def main():

    low = 29
    full = 97

    # You may override levels given above with arguments: [low <value>] [full <value>]
    for i in range(len(sys.argv)):
        a = sys.argv[i]
        if a == 'low':
            try:
                low = int(sys.argv[i + 1])
            except ValueError:
                pass

        """if a == 'full':
            try:
                full = int(sys.argv[i + 1])
            except ValueError:
                pass"""

    status = upower()

    if status["percentage"] is not None and status["percentage"] <= low and not status["charging"]:
        # notify("Battery low: " + str(status["percentage"]) + "%", status["icon_name"])
        subprocess.call(['obhud --battery LOW'], shell=True)

    """elif status["percentage"] is not None and status["percentage"] >= full and status["charging"]:
        # notify("Battery full: " + str(status["percentage"]) + "%", status["icon_name"])
        subprocess.call(['obhud --battery full'], shell=True)"""


def upower():
    """
    parse `upower -d` command output
    :return: dictionary
    """
    percentage = None
    charging = False
    icon_name = ''

    upower_output = subprocess.check_output("upower -d", shell=True).decode("utf-8").splitlines()
    for line in upower_output:
        line = line.strip()
        if line.startswith('percentage:'):
            try:
                percentage = int(line.split()[1][:-1])
            except ValueError:
                pass

        if line.startswith('state:'):
            charging = line.split()[1] != 'discharging'

        if line.startswith('icon-name:'):
            icon_name = line.split()[1][1:-1]  # strip quotes

    return {
        "percentage": percentage,
        "charging": charging,
        "icon_name": icon_name
    }


def notify(text, icon):
    subprocess.Popen(['notify-send', text, '-i', icon])


if __name__ == "__main__":
    main()