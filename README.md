# swayinfo
This is an attempt to reproduce my complete i3 workplace in the Sway environment. The scripts I find "stable" enough
to share, include description in the file header. For them all to work, you need packages as below:

- sway, swayinfo, swayidle
- py3status, py3status-modules, python-pytz, python-tzlocal
- swayshot
- light
- wmname
- python-i3ipc
- python-xlib
- wget

## Dynamic workspace names

This script uses the python `i3ipc` module to dynamically rename workspaces after the currently active window name. 
The name is prepended with either tiling mode (horizontal / vertical) or floating indicator.

### i3ipc-python module version

If you're lucky to use the 2.0.1 version of the library (released 26th August, 2019), 
the [wsdnames-i3ipc-2.0.1.py](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames-i3ipc-2.0.1.py) script
is all you need. It should work well on both sway and i3. Otherwise you may temporarily use the old 
[wsdnames.py](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames.py) script.

*NOTE: it's strongly recommended to use i3ipc-python v2.0.1. The old wsdnames.py script contains a bug which may cause
looping on i3. Since all my machines already run v2.0.1, the bug won't be fixed.*

**i3ipc-python 1.7.1 crashes on the 'binding' event in Sway**

That's why in the old version of the script ([wsdnames.py](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames.py)) 
the line which subscribes to the binding event has been commented out.

The bug described above does not affect i3. You may (and should) uncomment the line:

```
# i3.on("binding", on_window_focus)
```

**Sway / i3 config file:**

Pay attention to the fact, that your workspaces need to be **numbered**, not **named** for the script to work. 

Use:

```bash
bindsym $mod+1 workspace number 1
```

instead of 

```bash
bindsym $mod+1 workspace 1
```

in your `~/.config/sway/config` or `~/.config/i3/config` file. 
See [example configs](https://github.com/nwg-piotr/swayinfo/tree/master/config).