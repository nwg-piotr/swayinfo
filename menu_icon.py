#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script, intended for sway window manager, displays a try icon w/ the system menu attached to it.
Since GTK menus are still buggy on sway, it needs a workaround to work properly: you need the autotiling.py script
launched first. Lines 33-34 do the job.
"""

import os
import subprocess
import sys
import gi
import fcntl
import tempfile

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, GLib, AppIndicator3

from i3ipc import Connection, Event
i3 = Connection()

my_icon = AppIndicator3.Indicator.new('menu_icon', 'start-here',
                                        AppIndicator3.IndicatorCategory.OTHER)

c_audio_video = []
c_development = []
c_education = []
c_game = []
c_graphics = []
c_network = []
c_office = []
c_science = []
c_settings = []
c_system = []
c_utility = []
c_other = []


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == '-H' or sys.argv[1].upper() == '--HELP':
            print('\nUsage: menu_icon.py [-r | --refresh]\n')
            sys.exit(0)

    # exit if already running, thanks to Slava V at https://stackoverflow.com/a/384493/4040598
    pid_file = os.path.join(tempfile.gettempdir(), 'menu_icon.pid')
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('\nScript already running, exiting...\n')
        sys.exit(0)

    my_icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    list_entries()
    menu = build_menu()
    my_icon.set_menu(menu)

    Gtk.main()


def build_menu():
    menu = Gtk.Menu()

    if c_audio_video:
        menu.append(sub_menu(c_audio_video, 'AudioVideo'))

    if c_development:
        menu.append(sub_menu(c_development, 'Development'))

    if c_education:
        menu.append(sub_menu(c_education, 'Education'))

    if c_game:
        menu.append(sub_menu(c_game, 'Games'))

    if c_graphics:
        menu.append(sub_menu(c_graphics, 'Graphics'))

    if c_network:
        menu.append(sub_menu(c_network, 'Network'))

    if c_office:
        menu.append(sub_menu(c_office, 'Office'))

    if c_science:
        menu.append(sub_menu(c_science, 'Science'))

    if c_settings:
        menu.append(sub_menu(c_settings, 'Settings'))

    if c_system:
        menu.append(sub_menu(c_system, 'System'))

    if c_utility:
        menu.append(sub_menu(c_utility, 'Utility'))

    if c_other:
        menu.append(sub_menu(c_other, 'Other'))
    
    item = Gtk.SeparatorMenuItem()
    menu.append(item)
    
    item = Gtk.MenuItem.new_with_label('Hide menu icon')
    item.connect('activate', close)
    menu.append(item)
    menu.show_all()

    return menu


def sub_menu(entries_list, name):
    item = Gtk.MenuItem.new_with_label(name)
    submenu = Gtk.Menu()
    for entry in entries_list:
        subitem = Gtk.MenuItem()
        hbox = Gtk.HBox()
        if entry.icon.startswith('/'):
            image = Gtk.Image.new_from_file(entry.icon)
        else:
            image = Gtk.Image.new_from_icon_name(entry.icon, Gtk.IconSize.MENU)
        label = Gtk.Label()
        label.set_text(entry.name)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(label, False, False, 4)
        subitem.add(hbox)
        subitem.connect('activate', launch, entry.exec)
        submenu.append(subitem)
    item.set_submenu(submenu)

    return item


def launch(item, command):
    print(item, command)
    subprocess.call([command], shell=True)


def list_entries():
    for f in os.listdir('/usr/share/applications'):
        _name, _exec, _icon, _categories = '', '', '', ''
        try:
            with open(os.path.join('/usr/share/applications', f)) as d:
                lines = d.readlines()
                for line in lines:
                    if line.startswith("["):
                        read_me = line.strip() == "[Desktop Entry]"
                        continue
                    if read_me:
                        if line.startswith('Name='):
                            _name = line.split('=')[1].strip()
                        if line.startswith('Exec='):
                            _exec = line.split('=')[1].strip()
                            if '%' in _exec:
                                _exec = _exec.split('%')[0].strip()
                        if line.startswith('Icon='):
                            _icon = line.split('=')[1].strip()
                        if line.startswith('Categories'):
                            _categories = line.split('=')[1].strip()

                if _name and _exec and _categories:
                    app = DesktopEntry(_name, _exec, _icon, _categories)

        except Exception as e:
            print(e)


class DesktopEntry(object):
    def __init__(self, name, exec, icon=None, categories=None):
        self.name = name
        self.exec = exec
        self.icon = icon
        self.categories = categories.split(';')[:-1] if categories else ["Other"]

        if 'Audio' in self.categories or 'Video' in self.categories:
            c_audio_video.append(self)
        if 'Development' in self.categories:
            c_development.append(self)
        if 'Education' in self.categories:
            c_education.append(self)
        if 'Game' in self.categories:
            c_game.append(self)
        if 'Graphics' in self.categories:
            c_graphics.append(self)
        if 'Network' in self.categories:
            c_network.append(self)
        if 'Office' in self.categories:
            c_office.append(self)
        if 'Science' in self.categories:
            c_science.append(self)
        if 'Settings' in self.categories:
            c_settings.append(self)
        if 'System' in self.categories:
            c_system.append(self)
        if 'Utility' in self.categories:
            c_utility.append(self)

        if self not in c_audio_video and self not in c_development and self not in c_education and self not in c_game \
                and self not in c_graphics and self not in c_network and self not in c_office and self not in c_science \
                and self not in c_settings and self not in c_system and self not in c_utility:
            
            c_other.append(self)


def close(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
