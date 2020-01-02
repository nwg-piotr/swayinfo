#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This is an attempt to create a menu that behaves decently on sway window manager
"""

import os
import tempfile
import fcntl
import sys
import subprocess

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo

from i3ipc import Connection

i3 = Connection()

c_audio_video, c_development, c_education, c_game, c_graphics, c_network, c_office, c_science, c_settings, c_system, \
    c_utility, c_other = [], [], [], [], [], [], [], [], [], [], [], []

win = None


class MainWindow(Gtk.Window):
    def __init__(self, dimensions):
        w, h = dimensions
        Gtk.Window.__init__(self)
        self.set_title('sway_gtk_menu')
        self.set_resizable(True)
        self.connect("destroy", Gtk.main_quit)
        self.connect("focus-out-event", self.die)
        self.connect("key-release-event", self.test)
        self.connect("button-press-event", self.test)
        self.connect('draw', self.draw)
        self.set_size_request(w, h)

        # Credits for transparency go to  KurtJacobson:
        # https://gist.github.com/KurtJacobson/374c8cb83aee4851d39981b9c7e2c22c
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.set_app_paintable(True)

        self.menu = None
        outer_box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.HBox(spacing=5)
        self.button = Gtk.Button.new_with_label('')
        # self.button = Gtk.Button.new_from_icon_name("start-here", Gtk.IconSize.SMALL_TOOLBAR)
        hbox.pack_start(self.button, False, False, 0)
        outer_box.add(hbox)
        self.add(outer_box)

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, 0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)
        
    def die(self, *args):
        terminate(None)
        
    def test(self, *args):
        print(args)
        terminate(None)


def main():
    # exit if already running, thanks to Slava V at https://stackoverflow.com/a/384493/4040598
    pid_file = os.path.join(tempfile.gettempdir(), 'sway_gtk_menu.pid')
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(0)

    list_entries()
    dimensions = display_dimensions()
    global win
    win = MainWindow(dimensions)
    win.menu = build_menu()
    win.show_all()
    GLib.timeout_add(1, force_floating)
    Gtk.main()


def display_dimensions():
    root = i3.get_tree()
    found = False
    f = root.find_focused()
    while not found:
        f = f.parent
        found = f.type == 'output'

    return f.rect.width, f.rect.height


def force_floating():
    try:
        my_window = i3.get_tree().find_named('^sway_gtk_menu*')[0]
        if my_window:
            i3.command('floating enable')
            GLib.timeout_add(300, open_menu)

            return False
        
    except:
        pass
        
    return True


def open_menu(*args):
    win.menu = build_menu()
    win.menu.popup_at_widget(win.button, Gdk.Gravity.CENTER, Gdk.Gravity.CENTER, None)
    

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

    item = Gtk.MenuItem.new_with_label('Close menu')
    item.connect('activate', terminate)
    menu.append(item)
    menu.connect("hide", win.die)
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
    subprocess.Popen('exec {}'.format(command), shell=True)
    terminate(None)


def terminate(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
