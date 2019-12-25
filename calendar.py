#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script acquires a date with `zenity --calendar` and opens it with calendar.google.com in Chromium
"""

import subprocess

try:
    date = subprocess.check_output('zenity --calendar', shell=True).decode("utf-8")
    d_m_y = date.split('.')
    day, month, year = d_m_y[0].strip(), d_m_y[1].strip(), d_m_y[2].strip()
    command = 'chromium https://calendar.google.com/calendar/r/day/{}/{}/{}'.format(year, month, day)
    subprocess.Popen(command, shell=True)
except subprocess.CalledProcessError:
    pass
