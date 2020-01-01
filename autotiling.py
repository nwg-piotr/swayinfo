#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script has been moved to its own repository: https://github.com/nwg-piotr/autotiling
and will no longer be updated here.
"""

from i3ipc import Connection, Event

i3 = Connection()


def switch_splitting(i3, e):
    try:
        con = i3.get_tree().find_focused()
        if con.floating:                         # We're on i3: on sway it would be None
            is_floating = '_on' in con.floating  # May be 'auto_on' or 'user_on'
            is_full_screen = con.fullscreen_mode == 1
        else:                                    # We are on sway
            is_floating = con.type == 'floating_con'
            # On sway on 1st focus the parent container returns 1, then forever the focused container itself
            is_full_screen = con.fullscreen_mode == 1 or con.parent.fullscreen_mode == 1

        is_stacked = con.parent.layout == 'stacked'
        is_tabbed = con.parent.layout == 'tabbed'

        # Let's exclude floating containers, stacked layouts, tabbed layouts and full screen mode
        if not is_floating and not is_stacked and not is_tabbed and not is_full_screen:
            new_layout = 'splitv' if con.rect.height > con.rect.width else 'splith'
            i3.command(new_layout)

        if con.name == 'waybar':
            i3.command('splitv')

    except Exception as e:
        print('Error: {}'.format(e))
        pass


def main():
    i3.on(Event.WINDOW_FOCUS, switch_splitting)
    i3.main()


if __name__ == "__main__":
    main()
