#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import i3ipc

max_width = 30

# Create the Connection object that can be used to send commands and subscribe
# to events.
i3 = i3ipc.Connection()

# Print the name of the focused window
focused = i3.get_tree().find_focused()
print('Focused window %s is on workspace %s' %
      (focused.name, focused.workspace().name))

# Query the ipc for outputs. The result is a list that represents the parsed
# reply of a command like `i3-msg -t get_outputs`.
outputs = i3.get_outputs()

print('Active outputs:')

for output in filter(lambda o: o.active, outputs):
    print(output.name)

# Send a command to be executed synchronously.
i3.command('focus left')

# Take all fullscreen windows out of fullscreen
for container in i3.get_tree().find_fullscreen():
    container.command('fullscreen')

# Print the names of all the containers in the tree
root = i3.get_tree()
print(root.name)
for con in root:
    print("***", con.name)


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(self, e):
    # The first parameter is the connection to the ipc and the second is an object
    # with the data of the event sent from i3.
    if e.current:
        print('Windows on this workspace:')
        for w in e.current.leaves():
            print(w.name)


# Dynamically name your workspaces after the current window class
def on_window_focus(i3, e):
    focused = i3.get_tree().find_focused()
    ws_name = "%s: %s" % (focused.workspace().num, focused.name)
    name = ws_name if len(ws_name) <= max_width else ws_name[:max_width - 1] + "…"
    i3.command('rename workspace to "%s"' % name)


# Subscribe to events
i3.on('workspace::focus', on_workspace_focus)
i3.on("window::focus", on_window_focus)
i3.on("window::title", on_window_focus)
i3.on("window::focus", on_window_focus)
i3.on("binding", on_window_focus)

# Start the main loop and wait for events to come in.
i3.main()
