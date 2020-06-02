#!/usr/bin/python3
# _*_ coding: utf-8 _*_

"""
A psutil-based command to display customizable system usage info in a single line, intended for Tint2 executors

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Website: http://nwg.pl
Project: https://github.com/nwg-piotr/psuinfo
License: GPL3

Inspired by https://github.com/tknomanzr/scripts/blob/master/tint2/executors/cpu.py by William Bradley (@tknomanzr)
"""

# 
# ⌚⌛◷

import sys
import psutil
from time import sleep
import os


def main():
    fahrenheit = False

    pcpu, avg, speed, freqs, temp, fans, b_time, memory, swap, disks_usage, which, ul, dl, xfer_start, xfer_finish, \
        path_to_icon, glyph, c_name= None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
        None, None, None, None

    output = ""

    for i in range(3000):
    
        try:
            temp = psutil.sensors_temperatures(fahrenheit)
        except Exception as e:
            print("Exception: {}".format(e))
            exit()

        for key, value in temp.items():
            """if key == "k10temp":
                print(key, end=": ")
                for item in value:
                    if item.label == "Tdie":
                        print(item.current, end=": ")"""
            if key == "amdgpu":
                print(key, end=": ")
                for item in value:
                    print(item.label, end=" ")
                    print(item.current, end="℃ ")

        print("")
        sleep(2)

    """
    output += ""
    if "k10temp" in temp.keys():
        # ryzen, multiple Die temperatures for threadripper/Epyc
        ryzen_die_temps = [sensor.current for sensor in temp["k10temp"] if sensor.label == 'Tdie']
        output += str(int(max(ryzen_die_temps)))
    if "coretemp" in temp.keys():
        # intel
        output += str(int(temp["coretemp"][0][1]))
    output += "℉" if fahrenheit else "℃"
    print(output)
    """


if __name__ == "__main__":
    main()
