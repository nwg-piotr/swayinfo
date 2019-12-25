#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script acquires a date with `zenity --calendar` and opens it in calendar.google.com with Chromium
"""

import subprocess

try:
    date = subprocess.check_output('zenity --calendar', shell=True).decode("utf-8")
    d_m_y = date.split('.')
    day, month, year = d_m_y[0], d_m_y[1], d_m_y[2]

    command = 'chromium https://calendar.google.com/calendar/r/month/{}/{}/{}'.format(year, month, day)
    subprocess.Popen(command, shell=True)
except subprocess.CalledProcessError:
    pass
