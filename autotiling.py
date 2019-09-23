#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script uses the i3ipc python module to switch the layout/split
for the currently focused window vertical / horizontal,
depending on the window dimensions. It works on both sway and i3 window managers.

Inspired by https://github.com/olemartinorg/i3-alternating-layout

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Dependencies: python-i3ipc>=2.0.1 (i3ipc-python)
"""

from i3ipc import Connection, Event

i3 = Connection()


def switch_splitting(i3, e):
    try:
        con = i3.get_tree().find_focused()
        # con.type == 'floating_con'        - indicates floating enabled in Sway
        # con.floating                      - may be equal 'auto_on' or 'user_on' in i3
        is_floating = con.type == 'floating_con' or con.floating and '_on' in con.floating

        # Let's exclude floating windows
        if not is_floating:
            new_layout = 'splitv' if con.rect.height > con.rect.width else 'splith'
            i3.command(new_layout)

    except Exception as e:
        print('Error: {}'.format(e))
        pass


def main():
    i3.on(Event.WINDOW_FOCUS, switch_splitting)
    i3.on(Event.WINDOW_NEW, switch_splitting)
    i3.main()


if __name__ == "__main__":
    main()
