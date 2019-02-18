
from . import Colorer
import logging
logger = logging.getLogger('StegoVeritas:InstallDeps')

import platform
import subprocess

import getpass

# What is required by stegoveritas?
required_packages = ['exiftool'. '7z']

def main():

    dist_name, dist_version, dist_id = platform.dist()
    
    if dist_name.lower() == 'ubuntu':
        ubuntu()

    else:
        logger.error('Unhandled distribution to install deps: {}'.format(', '.join(platform.dist())))
        logger.error('Please poke me or submit a PR.')
        return

def ubuntu():
    
    packages = ['libimage-exiftool-perl', 'libexempi3', 'p7zip-full']

    subprocess.run(command_start + ['apt-get','update'])
    subprocess.run(command_start + ['apt-get','install','-y'] + packages)


# Standardize using sudo or not
command_start = ['sudo'] if getpass.getuser() != 'root' else []

if __name__ == '__main__':
    main()
