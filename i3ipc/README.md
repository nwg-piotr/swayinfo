## i3ipc-python 1.7.1 broken if it comes to Sway

The bug which crashes i3ipc on Sway has already been fixed by the library developers, but no updated version has been 
released so far. You need to find a -git package for you Linux distribution, if possible.

### Arch Linux

Use the [i3ipc-python-git](https://aur.archlinux.org/packages/i3ipc-python-git) AUR package.

### Void Linux

Since it's no way to create a -git package for Void, I built a temporary `python3-i3ipc-1.7.1_1.noarch.xbps` package,
which includes the necessary fixes for Sway. Download it and install from a local repository. 

```bash
$ xbps-rindex -a /path/to/local-repo/*.xbps
$ xbps-install -S python3-i3ipc --repository=/path/to/local-repo
```