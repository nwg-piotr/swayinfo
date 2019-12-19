#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script uses the i3ipc python library to display gtk3 AppIndicator3 tray icon + menu w/ the scratchpad content.
No AppIndicator3.IndicatorStatus other than ACTIVE has been used here, since it does not (yet?) work on sway:
it only displays the icon defined with indicator.set_icon_full.

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Dependencies: 'gtk3' 'libappindicator-gtk3' 'python' 'python-gobject' 'python-i3ipc'
"""

import sys
import subprocess
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from i3ipc import Connection

indicator = AppIndicator3.Indicator.new('scratchpad_indicator', '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
content_titles = []
e_menu = None

# edit paths according to your icons location
ICON_EMPTY: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_empty.png'
ICON_SINGLE: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_single.png'
ICON_MULTIPLE: str = '/home/piotr/PycharmProjects/swayinfo/icons/scratchpad_multiple.png'


def main():
    interval = 1000
    try:
        interval = int(sys.argv[1])
        if interval < 500:
            interval = 500
    except:
        pass
    
    connection = Connection()

    global indicator, e_menu
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
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
    
    if len(content_titles) > 0:
        item = Gtk.SeparatorMenuItem()
        menu.append(item)

    item = Gtk.MenuItem.new_with_label('Close indicator')
    item.connect('activate', quit)
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
        item.connect('activate', quit)
        self.append(item)
        self.show_all()


def show_scratchpad(item, title):
    title = title.replace(" ", "\\s")
    cmd = 'i3-msg [title="^{}*"] scratchpad show'.format(title)
    subprocess.check_output(cmd, shell=True)


def check_scratchpad(connection):
    global content_titles, indicator, e_menu
    current_titles = []
    
    scratchpad = connection.get_tree().find_named('__i3_scratch')
    leaves = scratchpad[0].floating_nodes
    
    for node in leaves:
        # find names on sway
        if node.name:
            current_titles.append(node.name)
        # find names on i3
        else:
            current_titles.append(node.nodes[0].name)
    
    if len(current_titles) > 0:

        if len(current_titles) == 1:
            indicator.set_icon_full(ICON_SINGLE, 'Scratchpad')
        else:
            indicator.set_icon_full(ICON_MULTIPLE, 'Scratchpad')

        if not current_titles == content_titles:
            content_titles = current_titles
            indicator.set_menu(build_menu())
    else:
        indicator.set_icon_full(ICON_EMPTY, 'Scratchpad')
        if indicator.get_menu():
            try:
                indicator.get_menu().is_empty
            except Exception as e:
                indicator.set_menu(e_menu)

        if len(content_titles) > 0:
            indicator.set_menu(build_menu())
            content_titles = []

    return True


def quit(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
