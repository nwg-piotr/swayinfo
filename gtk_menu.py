import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from i3ipc import Connection

i3 = Connection()


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('sway_gtk_menu')
        self.button = Gtk.Button.new_with_label("Close")
        self.button.connect("clicked", terminate)
        self.add(self.button)


def main():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    GLib.timeout_add(1, force_floating)
    Gtk.main()


def force_floating():
    try:
        my_window = i3.get_tree().find_named('^sway_gtk_menu*')[0]

        print(my_window.name)
        i3.command('floating on')
        #i3.command('splith')

        return False
        
    except:
        pass
        
    return True


def terminate(_):
    Gtk.main_quit()


if __name__ == "__main__":
    main()
