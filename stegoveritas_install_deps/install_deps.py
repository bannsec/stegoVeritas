
from . import Colorer
import logging
logger = logging.getLogger(__name__)

import subprocess
import distro

import getpass

# What is required by stegoveritas?
required_packages = ['exiftool', '7z', 'foremost']

def main():

    dist_name = distro.name().lower()

    if dist_name in ['ubuntu', 'debian', 'kali', 'debian gnu/linux', 'kali gnu/linux', 'pop!_os', 'elementary os',
                     'deepin', 'pureos', 'linux mint']:
        debian()

    elif dist_name == 'fedora':
        fedora()

    elif dist_name in ['archlinux', 'arch', 'arch linux', 'manjaro', 'manjaro linux']:
        archlinux()

    elif dist_name == 'parrot gnu/linux':
        parrot()

    else:
        logger.error('Unhandled distribution to install deps: {}'.format(dist_name))
        logger.error('Please poke me or submit a PR.')
        return

def debian():

    packages = ['libimage-exiftool-perl', 'libexempi*', 'p7zip-full', 'foremost', 'steghide', 'libmagic1']

    subprocess.run(command_start + ['apt-get','update'])
    subprocess.run(command_start + ['apt-get','install','-y'] + packages)

def fedora():

    packages = ['perl-Image-ExifTool', 'exempi', 'p7zip-plugins', 'foremost', 'steghide']

    subprocess.run(command_start + ['yum','install','-y'] + packages)

def archlinux():

    packages = ['perl-image-exiftool', 'p7zip', 'foremost', 'steghide', 'exempi']

    subprocess.run(command_start + ['pacman','-Syu'])
    subprocess.run(command_start + ['pacman','-S'] + packages)

def parrot():

    packages = ['exempi', 'libimage-exiftool-perl', 'p7zip-full', 'foremost', 'steghide']

    subprocess.run(command_start + ['apt-get','update'])
    subprocess.run(command_start + ['apt-get','install','-y'] + packages)

# Standardize using sudo or not
command_start = ['sudo'] if getpass.getuser() != 'root' else []

if __name__ == '__main__':
    main()
