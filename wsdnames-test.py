#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
EXPERIMENTAL, MAY OR MAY NOT WORK FOR YOU!

Dynamic workspace names for Sway
Development version: run with `-l | log` argument to enable logging to ~/.wsdnames/log.txt

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Depends on: i3ipc-python
"""

import i3ipc
import logging
import os
import sys

# truncate workspace name to this value
max_width = 30

# Create the Connection object that can be used to send commands and subscribe to events.
i3 = i3ipc.Connection()

splitv_text = 'V'
splith_text = 'H'

log_dir = os.getenv("HOME") + "/.wsdnames"
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
log_file = log_dir + "/log.txt"

logs = False


# A glyph will substitute the WS name if no window active, otherwise it'll be prepended to the window name
# Add more if you use more than 8 workspaces
def glyph(ws_number):
    glyphs = ["", "", "", "", "", "", "", ""]
    # Or you may use words instead of glyphs:
    # glyphs = ["HOME", "WWW", "FILE", "GAME", "TERM", "PIC", "TXT", "CODE"]
    try:
        return glyphs[ws_number - 1]
    except IndexError:
        return "?"


# Give the workspace a generic name: "number: glyph" (like "1: ")
def on_workspace_focus(self, e):
    try:
        con = i3.get_tree().find_focused()
        ws_num = con.workspace().num
        ws_new_name = "%s: %s" % (ws_num, glyph(ws_num))

        i3.command('rename workspace to "{}"'.format(ws_new_name))

    except Exception as ex:
        if logs:
            logging.error("on_workspace_focus: %s") % ex
        else:
            pass


# Name the workspace after the focused window name
def on_window_focus(i3, e):
    try:
        con = i3.get_tree().find_focused()
        # con.type == 'floating_con'        - indicates floating enabled in Sway
        # con.floating                      - may be equal 'auto_on' or 'user_on' in i3
        is_floating = con.type == 'floating_con' or con.floating and '_on' in con.floating

        # ⇢⇣⇉⇊⍈⍗◑◒☞☟⿰⿱     - these symbols display well in DejaVu Sans

        # Tiling mode or floating indication
        layout = con.parent.layout
        if layout == 'splith':
            split_text = '⇢' if not is_floating else ''
        elif layout == 'splitv':
            split_text = '⇣' if not is_floating else ''
        else:
            split_text = ''

        ws_old_name = con.workspace().name
        ws_name = "%s: %s\u00a0%s %s " % (con.workspace().num, glyph(con.workspace().num), split_text, con.name)
        name = ws_name if len(ws_name) <= max_width else ws_name[:max_width - 1] + "…"

        i3.command('rename workspace "%s" to %s' % (ws_old_name, name))

    except Exception as ex:
        if logs:
            logging.error("on_window_focus: %s") % ex
        else:
            pass


# In sway it's possible to open a new window w/o moving focus; let's give the workspace a name anyway.
def on_window_new(i3, e):
    try:
        con = i3.get_tree().find_by_id(e.container.id)
        ws_num = con.workspace().num
        w_name = con.name if con.name else ''

        if w_name and ws_num:
            name = "%s: %s\u00a0%s" % (ws_num, glyph(ws_num), w_name)
            i3.command('rename workspace "%s" to %s' % (ws_num, name))
        else:
            logging.warning('on_window_new: WS number or window name unknown')

    except Exception as ex:
        if logs:
            logging.error("on_window_new: %s") % ex
        else:
            pass


def main():
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "-l" or arg == "--log":
                global logs
                logs = True
    if logs:
        logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', filemode='w',
                            level=logging.DEBUG)
        logging.info('Starting wsdnames')

    # Subscribe to events
    i3.on('workspace::focus', on_workspace_focus)
    i3.on("window::focus", on_window_focus)
    i3.on("window::title", on_window_focus)
    i3.on("window::close", on_workspace_focus)
    i3.on("window::new", on_window_new)
    i3.on("binding", on_window_focus)

    # Start the main loop and wait for events to come in
    i3.main()


if __name__ == "__main__":
    main()
