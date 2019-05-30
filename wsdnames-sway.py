#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
Dynamic workspace names for Sway
WILL NOT WORK WELL ON i3!

Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/swayinfo
License: GPL3

Depends on: i3ipc-python
"""

import i3ipc

# truncate workspace name to this value
max_width = 30

# Create the Connection object that can be used to send commands and subscribe to events.
i3 = i3ipc.Connection()


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
    con = i3.get_tree().find_focused()
    ws_num = con.workspace().num
    ws_new_name = "%s: %s" % (ws_num, glyph(ws_num))

    i3.command('rename workspace to "{}"'.format(ws_new_name))


# Name the workspace after the focused window name
def on_window_focus(i3, e):
    con = i3.get_tree().find_focused()
    ws_old_name = con.workspace().name
    ws_name = "%s: %s\u00a0%s" % (con.workspace().num, glyph(con.workspace().num), con.name)
    name = ws_name if len(ws_name) <= max_width else ws_name[:max_width - 1] + "…"

    i3.command('rename workspace "%s" to %s' % (ws_old_name, name))


# In sway it's possible to open a new window w/o moving focus; let's give the workspace a name anyway.
def on_window_new(i3, e):
    con = i3.get_tree().find_by_id(e.container.id)
    ws_num = con.workspace().num
    w_name = con.name if con.name else ''

    if w_name and ws_num:
        name = "%s: %s\u00a0%s" % (ws_num, glyph(ws_num), w_name)
        i3.command('rename workspace "%s" to %s' % (ws_num, name))


# Subscribe to events
i3.on('workspace::focus', on_workspace_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::title", on_window_focus)
i3.on("window::close", on_workspace_focus)
i3.on("window::new", on_window_new)

# Start the main loop and wait for events to come in
i3.main()
