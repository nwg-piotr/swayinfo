#!/usr/bin/python3
# _*_ coding: utf-8 _*_

# 
# ⌚⌛◷
# 

import datetime
import psutil

b = ""


def main():
    print_time()
    print_battery()


def print_time():
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"), end=" ")


def print_battery():

    battery = psutil.sensors_battery()
    percent = int(battery.percent)

    if battery.power_plugged:
        print(b[0], end=" ")
    else:
        if percent <= 20:
            print(b[1], end=" ")
        elif percent <= 50:
            print(b[2], end=" ")
        elif percent <= 60:
            print(b[3], end=" ")
        elif percent <= 90:
            print(b[4], end=" ")
        else:
            print(b[5], end=" ")

    print(str(percent) + '%', end=" ")


if __name__ == "__main__":
    main()
