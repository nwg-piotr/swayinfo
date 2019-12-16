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

indicator = AppIndicator3.Indicator.new('arch_update_notifier', '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
pacman, aur = [], []
sway = False


def main():
    global indicator, sway
    try:
        result = subprocess.run(['swaymsg', '-t', 'get_seats'], stdout=subprocess.DEVNULL)
        sway = result.returncode == 0
    except:
        sway = False

    indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch.png', 'Up to date')
    indicator.set_attention_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch-attention.png',
                                      'Updates pending')
    # setting status 'PASSIVE' does not hide the tray icon on sway. Let's leave it always visible, if so.
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu())

    check_updates()
    GLib.timeout_add_seconds(300, check_updates)
    Gtk.main()


def menu():
    menu = Gtk.Menu()

    command_one = Gtk.MenuItem.new_with_label('Update')
    command_one.connect('activate', note)
    menu.append(command_one)
    exittray = Gtk.MenuItem.new_with_label('Close notifier')
    exittray.connect('activate', quit)
    menu.append(exittray)
    menu.show_all()
    return menu


def note(_):
    d = DialogExample(None)
    response = d.run()

    if response == Gtk.ResponseType.OK:
        print("The OK button was clicked")
    elif response == Gtk.ResponseType.CANCEL:
        print("The Cancel button was clicked")

    d.destroy()


def check_updates():
    global indicator, pacman, aur
    try:
        pacman = subprocess.check_output("checkupdates", shell=True).decode("utf-8").splitlines()
    except:
        pass

    try:
        aur = subprocess.check_output("trizen -Qqu -a", shell=True).decode("utf-8").splitlines()
    except:
        pass
    print(pacman)
    print(aur)

    if len(pacman) > 0 or len(aur) > 0:
        indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        # So far setting status does not change the icon in sway. Let's do it manually.
        if sway:
            indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch-attention.png',
                                    'Updates pending')
    else:
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        if sway:
            indicator.set_icon_full('/home/piotr/PycharmProjects/swayinfo/icons/arch.png',
                                    'Up to date')
    return True


class DialogExample(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        self.set_border_width(10)

        p = '<b>pacman:\n\n</b>'
        p += "\n".join(pacman)
        label = Gtk.Label()
        label.set_property('margin', 10)
        label.set_markup(p)

        box = self.get_content_area()

        box.add(label)
        self.show_all()


def quit(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
