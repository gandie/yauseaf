#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Lars Bergmann
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
main module of yauseaf firing commands on terminal
'''

import os
import sys
import subprocess


def erase(device):
    '''erase all existing data from device by filling the device from /dev/zero
    sudo dd status=progress if=/dev/zero of=/dev/sdb bs=4k && sync
    '''
    print(
        'Will erase device %s using dd. This may take a while, please be'
        ' patient.' % device
    )

    # of=/dev/sdX
    output_file = 'of=%s' % device

    subprocess.call(
        ['dd', 'status=progress', 'if=/dev/zero', output_file, 'bs=4k']
    )

    subprocess.call(
        ['sync']
    )

    print('Erasing device %s done.')


def make_partition(device):
    '''create a new partition table on the device with and a primary partition
    '''
    print(
        'Will create partition table and primary partition for device %s' % device
    )

    subprocess.call(
        ['parted', '-s', device, 'mklabel', 'msdos']
    )

    subprocess.call(
        [
            'parted', '-a', 'optimal', '-s', device, 'mkpart', 'primary', '0%',
            '100%'
        ]
    )

    print('Partition creation done.')


def make_filesystem(device, filesystem, label):
    '''create filesystem on new partition'''
    print('Will create %s filesystem with label %s on device %s' % (filesystem, label, device))

    maker = 'mkfs.%s' % filesystem

    if filesystem == 'ext4':
        subprocess.call(
            [maker, '-q', '-F', '-F', '-L', label, device + '1']
        )
    elif filesystem == 'ntfs':
        subprocess.call(
            [maker, '-q', '-f', '-F', '-F', '-L', label, device + '1']
        )

    subprocess.call(
        ['sync']
    )

    subprocess.call(
        ['sleep', '5']
    )

    print('Filesystem creation done.')


def unmount(device):
    '''make sure usb stick is not mounted'''
    subprocess.call(
        ['umount', device + '1']
    )


def create_mountpoint(user, label, device):
    '''create mountpoint directory for given user, mount new partition,
    change owner of directory, unmount and remove directory'''
    directory = '/media/%s/%s' % (user, label)

    print('Will create mountpoint in %s' % directory)

    subprocess.call(
        ['mkdir', directory]
    )

    subprocess.call(
        ['mount', device + '1', directory]
    )

    user_group = '%s:%s' % (user, user)

    subprocess.call(
        ['chown', '-R', user_group, directory]
    )

    subprocess.call(
        ['eject', device]
    )

    subprocess.call(
        ['rm', '-rf', directory]
    )

    print('Mountpoint created in %s' % directory)


def root_check():
    '''check if we were called with root privileges needed for most operations.
    return True if we are root.
    '''
    return os.getuid() == 0


def main(args):
    '''main function to decide what to be done with arguments'''
    if not root_check():
        print('Please call me using sudo ... . Root privileges required.')
        sys.exit(1)

    unmount(args.device)

    if args.erase:
        erase(args.device)

    make_partition(args.device)
    make_filesystem(args.device, args.filesystem, args.label)

    create_mountpoint(args.user, args.label, args.device)

    print('Done. Re-plugin stick and have fun!')
