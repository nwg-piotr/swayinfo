#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This code has just been started and is far from any usability at the moment. Come back later!
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib


indicator = AppIndicator3.Indicator.new('customtray', 'archlinux', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)


def main():
    global indicator

    indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch.png', 'Up to date')
    indicator.set_attention_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch-attention.png', 'Updates pending')
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu())
    GLib.timeout_add_seconds(3, test)
    Gtk.main()


def menu():
    menu = Gtk.Menu()

    command_one = Gtk.MenuItem.new_with_label('My Notes')
    command_one.connect('activate', note)
    menu.append(command_one)
    exittray = Gtk.MenuItem.new_with_label('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
    menu.show_all()
    return menu


def note(_):
    global indicator
    print(indicator.get_status() == AppIndicator3.IndicatorStatus.ACTIVE)


def test():
    global indicator
    if indicator.get_status() == AppIndicator3.IndicatorStatus.ATTENTION:
        indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch-attention.png', 'Updates pending')
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    else:
        indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch.png', 'Up tp date')
        indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
    return True


def quit(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
