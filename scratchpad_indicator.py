#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This code has just been started and is far from any usability at the moment. Come back later!
"""

import subprocess
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from i3ipc import Connection

indicator = None
content_names = []


def main():
    i3 = Connection()

    global indicator, sway
    try:
        result = subprocess.run(['swaymsg', '-t', 'get_seats'], stdout=subprocess.DEVNULL)
        sway = result.returncode == 0
    except:
        sway = False

    check_scratchpad(i3)
    GLib.timeout_add(3000, check_scratchpad, i3)
    Gtk.main()


def menu():
    menu = Gtk.Menu()

    item = Gtk.MenuItem.new_with_label('Update')
    item.connect('activate', note)
    menu.append(item)
    
    item = Gtk.MenuItem.new_with_label('Close notifier')
    item.connect('activate', quit)
    menu.append(item)

    menu.show_all()
    return menu


def note(_):
    pass


def check_scratchpad(connection):
    global content_names, indicator
    content_names = []
    
    scratchpad = connection.get_tree().find_named('__i3_scratch')
    leaves = scratchpad[0].floating_nodes
    
    for node in leaves:
        content_names.append(node.name)
    
    if len(content_names) > 0:
        if not indicator:
            indicator = AppIndicator3.Indicator.new('scratchpad_indicator', '',
                                                    AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        if len(content_names) == 1:
            indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/scratchpad.png', 'Scratchpad')
        else:
            indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/scratchpad2.png', 'Scratchpad')
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        indicator.set_menu(menu())
        
    else:
        if indicator:
            pass
        # todo hide indicator in some way here! Setting status PASSIVE does not work on sway.
    
    print(content_names)
    return True


def quit(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
