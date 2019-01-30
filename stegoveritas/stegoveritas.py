#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.WARN)

logger = logging.getLogger('StegoVeritas')

# TODO: Implement multi-threading pool: https://docs.python.org/3/library/concurrent.futures.html

import binascii
import os, os.path
import argparse
from .config import *
from .version import version

class StegoVeritas(object):

    def __init__(self, args=None):
        """
        Args:
            args (list, optional): Arguments as if you passed them via the command line (i.e.: ['-out','directory','-meta'])
        """
        
        #self._preflight()
        self._parse_args(args)
        self.modules = []

    def _parse_args(self, args=None):

        parser = argparse.ArgumentParser(description='Yet another Stego tool')
        parser.add_argument('-out',metavar='dir',type=str, help='Directory to place output in. Defaults to ./results',default=os.path.abspath('./results'))
        parser.add_argument('-meta',action='store_true',help='Check file for metadata information')
        parser.add_argument('-imageTransform',action='store_true',help='Perform various image transformations on the input image and save them to the output directory')
        parser.add_argument('-bruteLSB',action='store_true',help='Attempt to brute force any LSB related stegonography.')
        parser.add_argument('-colorMap',nargs="*",metavar='N',type=int,help='Analyze a color map. Optional arguments are colormap indexes to save while searching')
        parser.add_argument('-colorMapRange',nargs=2,metavar=('Start','End'),type=int,help='Analyze a color map. Same as colorMap but implies a range of colorMap values to keep')
        parser.add_argument('-extractLSB',action='store_true',help='Extract a specific LSB RGB from the image. Use with -red, -green, -blue, and -alpha')
        parser.add_argument('-red',nargs='+',metavar='index',type=int)
        parser.add_argument('-green',nargs='+',metavar='index',type=int)
        parser.add_argument('-blue',nargs='+',metavar='index',type=int)
        parser.add_argument('-alpha',nargs='+',metavar='index',type=int)
        parser.add_argument('-trailing',action='store_true',help='Check for trailing data on the given file')
        parser.add_argument('-debug', action='store_true', help='Enable debugging logging.')
        parser.add_argument('file_name',metavar='file',type=str, default=False, help='The file to analyze')

        self.args = parser.parse_args(args)

        if self.args.debug:
            logging.root.setLevel(logging.DEBUG)

        self.file_name = self.args.file_name
        self.results_directory = self.args.out


        """
        fType,fArray = openFile(fileName)

        printFileInformation(fType,fArray)
        args.outDir = args.outDir[0]

    if fType == "Image":
            import modules.image
            modules.image.run(fArray,args)

        """

    def run(self):
        """Run analysis on the file."""
        for module in modules.iter_modules(self):
            print('Running Module: ' + module.__class__.__name__)
            print(module.description)
            module.run()
            self.modules.append(module)

    
    ##############
    # Properties #
    ##############

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str) -> None:
        
        full_path = os.path.abspath(file_name)
        
        if not os.path.exists(full_path):
            logger.error('Cannot find file "{}"'.format(full_path))
            exit(1)

        logger.info('Analyzing file: ' + full_path)
        self.__file_name = full_path

    @property
    def results_directory(self) -> str:
        return self.__results_directory

    @results_directory.setter
    def results_directory(self, results_directory: str) -> None:
        full_path = os.path.abspath(results_directory)

        if os.path.exists(full_path) and not os.path.isdir(full_path):
            logger.error('Output path exists and is not a directory.')
            exit(1)

        os.makedirs(full_path, exist_ok=True)
        
        logger.info('Results Directory: ' + full_path)
        self.__results_directory = results_directory

    @property
    def modules(self) -> list:
        """list: List of all modules that have been run. NOTE: This will only be populated AFTER 'run' has been called and the modules themselves have been run."""
        return self.__modules

    @modules.setter
    def modules(self, modules):
        self.__modules = modules


def main(args=None):
    veritas = StegoVeritas(args=args)
    veritas.run()

from . import modules

if __name__ == '__main__':
    main()
