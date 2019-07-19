# i3ipc-python 1.7.1 is broken

The bug which crashes i3ipc on Sway [has already been fixed](https://github.com/acrisci/i3ipc-python/pull/105), but
no updated version has been released yet. While waiting for a new version, let's fix 1.7.1 temporarily.

### Void Linux

Since it's no way to create a -git package for Void, I built a temporary `python3-i3ipc-1.7.1_1.noarch.xbps` package,
which includes the necessary fixes for Sway. See https://voidlinux.org/usage/xbps for instructions on how to create
a local repository to install side downloaded packages.