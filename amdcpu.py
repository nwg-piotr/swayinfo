#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import psutil

min_freq = 1200
max_freq = 4000


def bar(values_per_core):
    # Looks good in DejaVuSansMono Nerd
    graph = "_▁▂▃▄▅▆▇█"

    string = ""
    for val in values_per_core:
        percentage = int(round(val / 10, 0))
        string += graph[percentage]

    return string


def main():
    error = "Unknown"
    try:
        frequencies = psutil.cpu_freq(True)
    except Exception as e:
        frequencies = None
        error = e

    if frequencies:
        values = []
        for freq in frequencies:
            current = freq.current
            f = current - min_freq
            if f < 0:
                f = 0
            value = f * 100 / max_freq
            values.append(value)

        print("{} {}%".format(bar(values), round(sum(values) / len(values), 1)))
    else:
        print("Error: {}".format(error))


if __name__ == "__main__":
    main()
