# Yet another usb stick eraser and formatter

Did you ever have problems formatting your usb stick using linux, e.g. Ubuntu?
Tired of buggy GUIs not doing their job?

No more! This tiny python program will fire just the right terminal commands
to erase your stick and put a filesystem of your trust on it.

Creating fresh usb sticks for daily usage has never been so easy!

Currently supports NTFS and EXT4 fileystems.

# Installation

```
python setup.py install
```

# Usage

```
usage: yauseaf [-h] [-f {ext4,ntfs}] [-L LABEL] [-U USER] [-e] device

A small python tool firing shell commands to erase and format usb sticks.

positional arguments:
  device                The device to be erased and formatted. CHOOSE THIS
                        CAREFULLY!

optional arguments:
  -h, --help            show this help message and exit
  -f {ext4,ntfs}, --filesystem {ext4,ntfs}
                        File system to use for usb-stick. Default is ext4.
  -L LABEL, --label LABEL
                        Label to use for new usb stick filesystem. Default is
                        USB-STICK
  -U USER, --user USER  User to create mountpoint for in /media/USER
  -e, --erase           Fill stick from /dev/zero before creating fileystem.
```
