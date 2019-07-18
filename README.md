# swayinfo
This is an attempt to reproduce my complete i3 workplace in the Sway environment. The scripts I find "stable" enough
to share, include description in the file header. For them all to work, you need packages as below:

- sway, swayinfo, swayidle
- py3status, py3status-modules, python-pytz, python-tzlocal
- swayshot
- light
- wmname
- python-i3ipc
- wget

## Dynamic workspace names

This script uses the `python-i3ipc` module to dynamically rename workspaces after the currently active window. 
The name is prepended with either tiling mode (horizontal / vertical) or floating indicator.

**i3ipc-python 1.7.1 crashes on the 'binding' event in Sway!**

That's why in the "stable" version of the script ([wsdnames.py](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames.py)) 
line #109 is commented out. The bug [has already been fixed](https://github.com/acrisci/i3ipc-python/pull/105), 
but the latest release does not yet contain the fix. If possible, you should use the -git version of the package.

**If you use i3 or fixed i3ipc.py library**, uncomment `i3.on("binding", on_window_focus)` in line 109.

**i3 / sway config file:**

Pay attention to the fact, that your workspaces need to be **numbered**, not **named** for the script to work. 

Use:

```bash
bindsym $mod+1 workspace number 1
```

instead of 

```bash
bindsym $mod+1 workspace 1
```

in your `~/.config/sway/config` file. See the [example config](https://github.com/nwg-piotr/swayinfo/blob/master/config/sway/config).