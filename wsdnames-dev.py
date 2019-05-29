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


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(self, e):
    focused = i3.get_tree().find_focused()
    ws_name = "%s: %s" % (focused.workspace().num, glyph(focused.workspace().num))
    i3.command('rename workspace to "%s"' % ws_name)


# Dynamically name your workspaces after the current window name
def on_window_focus(i3, e):
    focused = i3.get_tree().find_focused()
    ws_num = focused.workspace().num
    ws_name = "%s: %s\u00a0%s" % (ws_num, glyph(ws_num), focused.name)
    name = ws_name if len(ws_name) <= max_width else ws_name[:max_width - 1] + "…"
    i3.command('rename workspace to "%s"' % name)


def on_window_new(i3, e):
    if e.container.window_class:
        w_name = e.container.window_class
    elif e.container.window_instance:
        w_name = e.container.window_instance
    elif e.container.window_role:
        w_name = e.container.window_role
    else:
        w_name = None

    # search and give name by window name
    if w_name:
        for workspace in i3.get_workspaces():
            if not workspace.visible and not workspace.focused and w_name in workspace.representation:
                ws_name = "{}: {}\u00a0{}".format(workspace.num, glyph(workspace.num), w_name)
                i3.command('rename workspace {} to {}'.format(workspace.num, ws_name))
    # search by window id
    else:
        if e.container.id:
            for workspace in i3.get_workspaces():
                if not workspace.visible and not workspace.focused and e.container.id == workspace.focus[0]:
                    ws_name = "{}: {}".format(workspace.num, glyph(workspace.num))
                    i3.command('rename workspace {} to {}'.format(workspace.num, ws_name))


# Subscribe to events
i3.on('workspace::focus', on_workspace_focus)
i3.on('window::new', on_window_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::title", on_window_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::new", on_window_new)
i3.on("window::close", on_workspace_focus)

# Start the main loop and wait for events to come in
i3.main()
