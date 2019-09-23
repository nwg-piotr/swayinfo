# swayinfo
This repository is my collection of scripts useful in the Sway and i3 environment. Some of them I find mature / useful
enough to share, and those are [Dynamic workspace names](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames-i3ipc-2.0.1.py)
and [Auto-tiling](https://github.com/nwg-piotr/swayinfo/blob/master/autotiling.py). If it comes to the rest - please
read descriptions inside. All the code was written in python3.

## [Dynamic workspace names](https://github.com/nwg-piotr/swayinfo/blob/master/wsdnames-i3ipc-2.0.1.py)

This script uses the python `i3ipc` module to dynamically rename workspaces after the currently active window name. 
The name is prepended with either tiling mode (horizontal / vertical) or floating indicator. 

[![Script in action](https://img.youtube.com/vi/Jh9K3F0O7lM/0.jpg)](https://www.youtube.com/watch?v=Jh9K3F0O7lM)

### i3ipc-python module

The script depends on the **[python i3ipc](https://github.com/altdesktop/i3ipc-python) module in version >= 2.0.1**. 
You need to install the package proper for your Linux distribution. In case you installed the library in other way, 
keep in mind that it also needs the `xlib` module (python-xlib) to work.

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

## [Vertical / horizontal auto-tiling](https://github.com/nwg-piotr/swayinfo/blob/master/autotiling.py)

This script was inspired by [i3 alternating layout script](https://github.com/olemartinorg/i3-alternating-layout) 
by olemartinorg, but uses the `i3ipc` module (see [above](https://github.com/nwg-piotr/swayinfo#i3ipc-python-module)) 
instead of `i3-py`, so works on both i3 and Sway. It switches layout/split for the currently focused window vertical 
/ horizontal, depending on the window dimensions.

[![Auto-tiling in action](https://img.youtube.com/vi/oK-C0kqsdAA/0.jpg)](https://www.youtube.com/watch?v=oK-C0kqsdAA)

## How to use:

Save the script anywhere, make executable and autostart in your i3/sway config file:

`exec /path/to/the/script/script-name.py`

on sway or

`exec --no-startup-id /path/to/the/script/script-name.py`

on i3.