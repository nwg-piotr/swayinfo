# swayinfo
This is an attempt to reproduce my complete i3 workplace in the Sway environment. The scripts I find "stable" enough
to share, include description in the file header. For them all to work you need packages as below:

- sway, swayinfo, swayidle
- py3status, py3status-modules, python-pytz, python-tzlocal
- swayshot
- light
- wmname
- python-i3ipc

## Dynamic workspace-names

This script uses the `python-i3ipc` module to dynamically rename workspaces after the currently active window. 
The name is prepended with either tiling mode (horizontal / vertical) or floating indicator.

The most recent version is the [wsdnames-sway-dev.py](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames-sway-dev.py) file.

The `i3ipc-python` may or may not exist for certain Linux distributions. For Arch Linux you'll find it in AUR.

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