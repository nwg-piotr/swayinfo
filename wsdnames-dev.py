#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
EARLY DEVELOPMENT VERSION, DON'T USE!

Dynamic workspace names
Based on the example code at https://pypi.org/project/i3ipc
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


# Give the workspace a generic name
def on_workspace_focus(self, e):
    con = i3.get_tree().find_focused()
    ws_name = "{}: {}".format(con.workspace().num, glyph(con.workspace().num))
    i3.command('rename workspace to "%s"' % ws_name)


# Name the workspace after the focused window name
def on_window_focus(i3, e):
    con = i3.get_tree().find_focused()
    ws_name = "{}: {}\u00a0{}".format(con.workspace().num, glyph(con.workspace().num), con.name)
    name = ws_name if len(ws_name) <= max_width else ws_name[:max_width - 1] + "…"
    i3.command('rename workspace to "%s"' % name)


# (Pre)name the workspace after the container name (if any)
def on_window_new(i3, e):
    w_name = e.container.name if e.container.name else ''
    con = i3.get_tree().find_by_id(e.container.id)
    name = "{}: {}\u00a0{}".format(con.workspace().num, glyph(con.workspace().num), w_name)
    i3.command('rename workspace {} to {}'.format(con.workspace().num, name))


# Subscribe to events
i3.on('workspace::focus', on_workspace_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::title", on_window_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::close", on_workspace_focus)
i3.on("window::new", on_window_new)  # [sway] if window opened in another WS and not focused

# Start the main loop and wait for events to come in
i3.main()
