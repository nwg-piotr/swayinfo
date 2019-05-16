#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script retrieves weather data from http://openweathermap.org © 2012 — 2018 OpenWeatherMap, Inc.
1. Obtain API key at http://openweathermap.org;
2. find your city ID at https://openweathermap.org/find;
3. enter both values in the ~/t2ecol/weatherrc file;
4. edit other values if necessary.

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Website: http://nwg.pl
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Arguments to override some ~/t2ecol/weatherrc config file values:

[-I<items>] [-A<api_key>] [-C<city_id>] [-U<metric>|<imperial>] [-L<lang>] [-D[<city_id>]]
items: [s]hort description, [d]escription, [t]emperature, [p]ressure, [h]umidity, [w]ind, [c]ity ID
-D[<city_id>] shows details as a notification.

*** THIS SCRIPT IS NOT YET READY! ***

Dependencies: wget
"""

import subprocess
import json
from collections import namedtuple
import locale
import os
import sys
import re
import time


def main():
    config_dir = os.getenv("HOME") + "/.config/swinfo"
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)
    response = None
    name = None

    settings = Settings(config_dir)

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):

            if sys.argv[i].upper() == '-H' or sys.argv[i].upper() == '--HELP':
                print_help()
                exit(0)

            if sys.argv[i].upper() == '-N':
                name = settings.dict["_weather"]

            if sys.argv[i].upper().startswith('-M'):
                name = sys.argv[i][2::]

            if sys.argv[i].startswith("-I"):
                settings.items = sys.argv[i][2::]

            if sys.argv[i].startswith("-A"):
                settings.api_key = sys.argv[i][2::]

            if sys.argv[i].startswith("-C"):
                settings.city_id = sys.argv[i][2::]

            if sys.argv[i].startswith("-U"):
                settings.units = sys.argv[i][2::]

            if sys.argv[i].startswith("-L"):
                settings.lang = sys.argv[i][2::]

            if sys.argv[i].startswith("-D"):
                c_id = sys.argv[i][2::]
                if c_id:
                    show_details(config_dir, c_id)
                else:
                    show_details(config_dir, settings.city_id)

    request_url = "http://api.openweathermap.org/data/2.5/weather?id=" + settings.city_id + "&appid=" + \
                  settings.api_key + "&units=" + settings.units + "&lang=" + settings.lang
    try:
        response = subprocess.check_output("wget -o /dev/null -qO- '" + request_url + "'", shell=True)

    except subprocess.CalledProcessError as exitcode:
        #if name is None:
        #    os.system("echo /usr/share/t2ec/refresh.svg")
        os.system("echo Exit code: " + str(exitcode.returncode))
        exit(0)

    if response is not None:
        # Convert JSON to object - after DS. at https://stackoverflow.com/a/15882054/4040598
        owm = json.loads(response, object_hook=lambda d: namedtuple('t', d.keys(), rename=True)(*d.values()))

        # Icon definitions. You may also use just characters here, like '' instead of '\uf00d'
        icons = {'01d': '\uf00d',
                 '01n': '\uf02e',
                 '02d': '\uf002',
                 '02n': '\uf031',
                 '03d': '\uf041',
                 '03n': '\uf041',
                 '04d': '\uf013',
                 '04n': '\uf013',
                 '09d': '\uf00b',
                 '09n': '\uf02b',
                 '10d': '\uf008',
                 '10n': '\uf028',
                 '11d': '\uf005',
                 '11n': '\uf025',
                 '13d': '\uf00a',
                 '13n': '\uf02a',
                 '50d': '\uf014',
                 '50n': '\uf014'}

        icon_sunrise = '\uf046'
        icon_sunset = '\uf047'
        icon_temperature = '\uf053'
        icon_humidity = '\uf078'
        icon_pressure = '\uf079'
        icon_wind = '\uf050'

        if owm.cod == 200:
            # Prepare panel items
            icon = '\uea61'
            try:
                icon = icons[str(getattr(owm.weather[0], "icon"))]
            except KeyError:
                pass

            city, s_desc, desc, temp, pressure, humidity, wind, deg, sunrise, sunset, cloudiness \
                = None, None, None, None, None, None, None, None, None, None, None

            try:
                city = str(owm.name + ", " + getattr(owm.sys, "country"))
            except AttributeError:
                pass

            try:
                s_desc = str(getattr(owm.weather[0], "main"))
            except AttributeError:
                pass

            try:
                desc = str(getattr(owm.weather[0], "description"))
            except AttributeError:
                pass

            unit = "°F" if settings.units == "imperial" else "°C"
            try:
                temp = str(round(float(str(getattr(owm.main, "temp"))), 1)) + unit
            except AttributeError:
                pass

            try:
                pressure = str(int(round(float(str(getattr(owm.main, "pressure"))), 0))) + " hpa"
            except AttributeError:
                pass

            try:
                humidity = str(int(round(float(str(getattr(owm.main, "humidity"))), 0))) + "%"
            except AttributeError:
                pass

            unit = " m/h" if settings.units == "imperial" else " m/s"
            try:
                wind = str(getattr(owm.wind, "speed")) + unit
            except AttributeError:
                pass

            try:
                deg = str(getattr(owm.wind, "deg"))
            except AttributeError:
                pass
            if deg is not None:
                wind += ", " + wind_dir(float(deg))

            # Values below will only be used in the details view (notification)
            try:
                sunrise = time.strftime('%H:%M', time.localtime(getattr(owm.sys, "sunrise")))
            except AttributeError:
                pass

            try:
                sunset = time.strftime('%H:%M', time.localtime(getattr(owm.sys, "sunset")))
            except AttributeError:
                pass

            try:
                cloudiness = str(getattr(owm.clouds, "all")) + "%"
            except AttributeError:
                pass

            output = icon

            for i in range(len(settings.items)):
                if settings.items[i] == "c" and city is not None:
                    output += " " + city + " "
                if settings.items[i] == "s" and s_desc is not None:
                    output += " " + s_desc + " "
                if settings.items[i] == "d" and desc is not None:
                    output += " " + desc + " "
                if settings.items[i] == "t" and temp is not None:
                    output += icon_temperature + " " + temp + " "
                if settings.items[i] == "p" and pressure is not None:
                    output += icon_pressure + " " + pressure + " "
                if settings.items[i] == "h" and humidity is not None:
                    output += icon_humidity + " " + humidity + " "
                if settings.items[i] == "w" and wind is not None:
                    output += icon_wind + " " + wind + " "
                if settings.items[i] == "S" and sunrise is not None and sunset is not None:
                    output += icon_sunrise + " " + sunrise + " " + icon_sunset + " " + sunset + " "

            print(re.sub(' +', ' ', output).strip())

            details = icon + "\n"
            if city is not None:
                details += settings.dict["_weather"] + " " + city + "\n"
            if temp is not None:
                details += temp
            if desc is not None:
                details += ", " + desc
            details += "\n"
            if wind is not None:
                details += settings.dict["_wind"] + ": " + wind + "\n"
            if cloudiness is not None:
                details += settings.dict["_cloudiness"] + ": " + cloudiness + "\n"
            if pressure is not None:
                details += settings.dict["_pressure"] + ": " + pressure + "\n"
            if humidity is not None:
                details += settings.dict["_humidity"] + ": " + humidity + "\n"
            if sunrise is not None:
                details += settings.dict["_sunrise"] + ": " + sunrise + "\n"
            if sunset is not None:
                details += settings.dict["_sunset"] + ": " + sunset + "\n"

            subprocess.call(["echo '" + str(details) + "' > " + config_dir + "/.weather-" + settings.city_id], shell=True)

        else:
            if name is None:
                os.system("echo /usr/share/t2ec/refresh.svg")
            os.system("echo HTTP status: " + str(owm.cod))
            exit(0)


def show_details(t2ec_dir, city):
    details = ""
    try:
        details = open(t2ec_dir + "/.weather-" + city, 'r').read().rstrip().splitlines()
    except FileNotFoundError:
        exit(0)

    if details:
        icon = details[0]
        title = details[1]
        message = '\n'.join(details[2:])
        message = message.replace("-", "\\-")

        os.system("notify-send '" + title + "' " + "'" + message + "' -i " + icon)


def print_help():

    print("\nFor multiple executors you may override /home/user/.t2ecol/weatherrc settings with arguments:")

    print("\nt2ec --weather [-I<items>] [-A<api_key>] [-C<city_id>] [-U<units>] [-L<lang>]")

    print("\n<items>: [s]hort description, [d]escription, [t]emperature, [p]ressure, [h]umidity, [w]ind, [c]ity name, [S]unrise/sunset")

    print("\nTo show details as a notification:")

    print("\nt2ec --weather -D[<city_id>]")

    print("\nAdd [<city_id>] if varies from weatherrc city_id field.\n")


class Settings:
    def __init__(self, config_dir):
        super().__init__()

        # Create settings file if not found
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)
        if not os.path.isfile(config_dir + "/weatherrc"):
            config = [
                "# Items: [s]hort description, [d]escription, [t]emperature, [p]ressure, [h]umidity, [w]ind, [c]ity name, [S]unrise & sunset\n",
                "# API key: go to http://openweathermap.org and get one\n",
                "# city_id you will find at http://openweathermap.org/find\n",
                "# units may be metric or imperial\n",
                "# Uncomment lang to override system $LANG value\n",
                "# \n",
                "# Delete this file if something goes wrong :)\n",
                "# \n",
                "items = ct\n",
                "api_key = your_key_here\n",
                "city_id = 2643743\n",
                "units = metric\n",
                "#lang = en\n",
                "\n",
                "# You may translate your output below:\n",
                "#\n",
                "_weather = Weather in\n",
                "_wind = Wind\n",
                "_cloudiness = Cloudiness\n",
                "_pressure = Pressure\n",
                "_humidity = Humidity\n",
                "_sunrise = Sunrise\n",
                "_sunset = Sunset"]

            subprocess.call(["echo '" + ''.join(config) + "' > " + config_dir + "/weatherrc"], shell=True)

        # Set default values
        self.items = "ct"
        self.api_key = ""
        self.city_id = "2643743"  # London, UK
        self.units = "metric"
        self.lang = None
        self.img_path = None
        self.dict = {'_weather': 'Weather',
                     '_wind': 'Wind',
                     '_cloudiness': 'Cloudiness',
                     '_pressure': 'Pressure',
                     '_humidity': 'Humidity',
                     '_sunrise': 'Sunrise',
                     '_sunset': 'Sunset'}

        # Override defaults with config file values, if found
        lines = open(config_dir + "/weatherrc", 'r').read().rstrip().splitlines()

        for line in lines:
            if not line.startswith("#"):
                if line.startswith("items"):
                    self.items = line.split("=")[1].strip()
                elif line.startswith("api_key"):
                    self.api_key = line.split("=")[1].strip()
                elif line.startswith("city_id"):
                    self.city_id = line.split("=")[1].strip()
                elif line.startswith("units"):
                    self.units = line.split("=")[1].strip()
                elif line.startswith("lang"):
                    self.lang = line.split("=")[1].strip()
                elif line.startswith("img_path"):
                    self.img_path = line.split("=")[1].strip()

                elif line.startswith("_weather"):
                    self.dict["_weather"] = line.split("=")[1].strip()
                elif line.startswith("_wind"):
                    self.dict["_wind"] = line.split("=")[1].strip()
                elif line.startswith("_cloudiness"):
                    self.dict["_cloudiness"] = line.split("=")[1].strip()
                elif line.startswith("_pressure"):
                    self.dict["_pressure"] = line.split("=")[1].strip()
                elif line.startswith("_humidity"):
                    self.dict["_humidity"] = line.split("=")[1].strip()
                elif line.startswith("_sunrise"):
                    self.dict["_sunrise"] = line.split("=")[1].strip()
                elif line.startswith("_sunset"):
                    self.dict["_sunset"] = line.split("=")[1].strip()

        if self.lang is None:
            try:
                loc = locale.getdefaultlocale()[0][:2]
            except TypeError:
                loc = ""
            self.lang = loc if loc else "en"


def wind_dir(deg):
    if deg >= 348.75 or deg <= 11.25:
        return "N"
    elif 11.25 < deg <= 33.75:
        return "NNE"
    elif 33.75 < deg <= 56.25:
        return "NE"
    elif 56.25 < deg <= 78.75:
        return "ENE"
    elif 78.75 < deg <= 101.25:
        return "E"
    elif 101.25 < deg <= 123.75:
        return "ESE"
    elif 123.75 < deg <= 146.25:
        return "SE"
    elif 146.25 < deg <= 168.75:
        return "SSE"
    elif 168.75 < deg <= 191.25:
        return "S"
    elif 191.25 < deg <= 213.75:
        return "SSW"
    elif 213.75 < deg <= 236.25:
        return "SW"
    elif 236.25 < deg <= 258.75:
        return "WSW"
    elif 258.75 < deg <= 281.25:
        return "W"
    elif 281.25 < deg <= 303.75:
        return "WNW"
    elif 303.75 < deg <= 326.25:
        return "NW"
    elif 326.25 < deg <= 348.75:
        return "NNW"
    else:
        return "WTF"


if __name__ == "__main__":
    main()