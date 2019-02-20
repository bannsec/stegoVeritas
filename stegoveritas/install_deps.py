
from . import Colorer
import logging
logger = logging.getLogger('StegoVeritas:InstallDeps')

import platform
import subprocess

import getpass

# What is required by stegoveritas?
required_packages = ['exiftool', '7z']

def main():

    dist_name, dist_version, dist_id = platform.dist()
    
    if dist_name.lower() in ['ubuntu', 'debian']:
        debian()

    elif dist_name.lower() == 'fedora':
        fedora()

    else:
        logger.error('Unhandled distribution to install deps: {}'.format(', '.join(platform.dist())))
        logger.error('Please poke me or submit a PR.')
        return

def debian():
    
    packages = ['libimage-exiftool-perl', 'libexempi3', 'p7zip-full']

    subprocess.run(command_start + ['apt-get','update'])
    subprocess.run(command_start + ['apt-get','install','-y'] + packages)

def fedora():
    
    packages = ['perl-Image-ExifTool', 'exempi', 'p7zip-plugins']

    subprocess.run(command_start + ['yum','install','-y'] + packages)

# Standardize using sudo or not
command_start = ['sudo'] if getpass.getuser() != 'root' else []

if __name__ == '__main__':
    main()
