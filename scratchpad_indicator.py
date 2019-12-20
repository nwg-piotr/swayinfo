#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script uses the i3ipc python library to display gtk3 AppIndicator3 tray icon + menu w/ the scratchpad content.
AppIndicator3.IndicatorStatus.PASSIVE will hide the icon on i3 only, until tray is fixed on sway.

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Dependencies: 'gtk3' 'libappindicator-gtk3' 'python' 'python-gobject' 'python-i3ipc'.

Also all /icons/scratchpad*.png files are necessary!

Command: scratchpad_indicator.py [refresh_interval_ms]
"""

import os
import sys
import gi
import fcntl
import tempfile

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from i3ipc import Connection

indicator = AppIndicator3.Indicator.new('scratchpad_indicator', '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
content_titles = []
e_menu = None
connection = None

# edit path according to where you saved the files
ICON_EMPTY: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_empty.png'
ICON_SINGLE: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_single.png'
ICON_MULTIPLE: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_multiple.png'


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == '-H' or sys.argv[1].upper() == '--HELP':
            print('\nUsage: scratchpad_indicator.py [refresh_rate_ms] (1000 by default)\n')
            sys.exit(0)
            
    # exit if already running, thanks to Slava V at https://stackoverflow.com/a/384493/4040598
    pid_file = os.path.join(tempfile.gettempdir(), 'scratch_indicator.pid')
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('\nScript already running, exiting...\n')
        sys.exit(0)

    # GLib timeout in miliseconds
    interval = 1000
    if len(sys.argv) > 1:
        if sys.argv[1].upper == '-H' or sys.argv[1].upper == '--HELP':
            print('Usage: scratchpad_indicator.py [refresh_rate_ms]')
        else:
            try:
                interval = int(sys.argv[1])
                if interval < 500:
                    interval = 500
            except:
                pass
    
    global connection
    connection = Connection()

    global indicator, e_menu
    indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
    indicator.set_icon_full(ICON_EMPTY, 'Scratchpad')

    e_menu = EmptyMenu()
    indicator.set_menu(e_menu)

    check_scratchpad(connection)

    GLib.timeout_add(interval, check_scratchpad, connection)
    Gtk.main()


def build_menu():
    """
    Build the tray icon menu out of names of windows found in scratchpad
    """
    global content_titles
    menu = Gtk.Menu()
    for title in content_titles:
        item = Gtk.MenuItem.new_with_label(title)
        item.connect('activate', show_scratchpad, title)
        menu.append(item)

    item = Gtk.SeparatorMenuItem()
    menu.append(item)

    item = Gtk.MenuItem.new_with_label('Close indicator')
    item.connect('activate', close)
    menu.append(item)
    menu.show_all()

    return menu


class EmptyMenu(Gtk.Menu):
    """
    Subclassed to add the 'is_empty' field, which - if found - prevents from setting the menu
    again and again if scratchpad empty.
    """
    def __init__(self):
        super().__init__()
        self.is_empty = True
        item = Gtk.MenuItem.new_with_label('Close indicator')
        item.connect('activate', close)
        self.append(item)
        self.show_all()


def show_scratchpad(item, title):
    """
    Shows a window selected from scratchpad by title
    """
    title = title.replace(" ", "\\s")
    cmd = '[title="^{}*"] scratchpad show'.format(title)
    global connection
    connection.command(cmd)


def check_scratchpad(connection):
    global content_titles, indicator, e_menu
    current_titles = []
    
    scratchpad = connection.get_tree().find_named('__i3_scratch')
    leaves = scratchpad[0].floating_nodes
    
    for node in leaves:
        # find names of windows in scratchpad (sway)
        if node.name:
            current_titles.append(node.name)
        # find names of windows in scratchpad (i3)
        else:
            current_titles.append(node.nodes[0].name)
    
    if len(current_titles) > 0:
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        if len(current_titles) == 1:
            indicator.set_icon_full(ICON_SINGLE, 'Scratchpad')
        else:
            indicator.set_icon_full(ICON_MULTIPLE, 'Scratchpad')

        if not current_titles == content_titles:
            content_titles = current_titles
            indicator.set_menu(build_menu())
    else:
        indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
        indicator.set_icon_full(ICON_EMPTY, 'Scratchpad')
        if indicator.get_menu():
            try:
                # Is the menu an instance of our EmptyMenu subclass?
                indicator.get_menu().is_empty
            except:
                indicator.set_menu(e_menu)

        if len(content_titles) > 0:
            indicator.set_menu(build_menu())
            content_titles = []

    return True


def close(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
