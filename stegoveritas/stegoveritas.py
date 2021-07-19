#!/usr/bin/env python3

from . import Colorer

import logging
logging.basicConfig(level=logging.WARN)

logger = logging.getLogger('StegoVeritas')

import binascii
import os
import argparse
from .version import version

import magic
import time
import shutil
from copy import copy

from stegoveritas_install_deps.install_deps import required_packages

import binwalk
import tempfile
import hashlib
import random

from .helpers import generate_nonce

from prettytable import PrettyTable


class StegoVeritas(object):

    def __init__(self, args=None):
        """
        Args:
            args (list, optional): Arguments as if you passed them via the command line (i.e.: ['-out','directory','-meta'])
        """

        self._preflight()
        self._parse_args(args)
        self.modules = []

        # For things we find inside test_output call
        self._keeper_directory = os.path.join(self.results_directory, 'keepers')
        os.makedirs(self._keeper_directory, exist_ok=True)

    def run(self):
        """Run analysis on the file."""
        for module in modules.iter_modules(self):
            print('Running Module: ' + module.__class__.__name__)
            print(module.description)
            module.run()
            self.modules.append(module)

    def test_output(self, thing):
        """
        Args:
            thing (bytes): Renerally from the dump functions
                ex: thing = b'\x01\x02\x03'

        Returns:
            Nothing. Move output into keep directory if it's worth-while


        Test if output is worth keeping. If it is, move it into the results directory.
        Initially, this is using the Unix file command on the output and checking for non "Data" returns
        """

        assert type(thing) == bytes, 'test_output got unexpected thing type of {}'.format(type(thing))

        # TODO: Test new logic...
        # TODO: Iterate through binary offset to find buried data

        #
        # File magic test
        #

        m = magic.from_buffer(thing, mime=True)

        # Generic Output
        if m != 'application/octet-stream':
            m = magic.from_buffer(thing, mime=False)
            print("Found something worth keeping!\n{0}".format(m))
            # Save it to disk
            with open(os.path.join(self._keeper_directory, str(time.time()) + "-" + generate_nonce()), "wb") as f:
                f.write(thing)

        #
        # binwalk test
        #

        # TODO: Update this to in-memory scanning if binwalk updates their stuff: https://github.com/ReFirmLabs/binwalk/issues/389
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_scan_file = os.path.join(tmpdirname, 'scanme')

            # Couldn't find a good 'output directory' option for binwalk. Changing dirs because of this.
            saved_dir = os.getcwd()
            os.chdir(tmpdirname)

            with open(tmp_scan_file, 'wb') as f:
                f.write(thing)

            table = PrettyTable(['Offset', 'Carved/Extracted', 'Description', 'File Name'])
            table.align = 'l'
            keepers = []

            # Run the scan
            for module in binwalk.scan(tmp_scan_file, signature=True, quiet=True, extract=True):
                for result in module.results:
                    if result.file.path in module.extractor.output:
                        if result.offset in module.extractor.output[result.file.path].carved:
                            table.add_row([hex(result.offset), 'Carved', result.description, os.path.basename(module.extractor.output[result.file.path].carved[result.offset])])
                            keepers.append(module.extractor.output[result.file.path].carved[result.offset])
                            # print("Carved data from offset 0x%X to %s" % (result.offset, module.extractor.output[result.file.path].carved[result.offset]))
                        if result.offset in module.extractor.output[result.file.path].extracted:
                            # print(result.offset, module.extractor.output[result.file.path].extracted)
                            table.add_row([hex(result.offset), 'Extracted', result.description, os.path.basename(module.extractor.output[result.file.path].extracted[result.offset].files[0])])
                            keepers += module.extractor.output[result.file.path].extracted[result.offset].files
                            # print("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(module.extractor.output[result.file.path].extracted[result.offset].files), result.offset, module.extractor.output[result.file.path].extracted[result.offset].files[0], module.extractor.output[result.file.path].extracted[result.offset].command))

            # If we found something
            if keepers != []:
                print(table)

                for keeper in keepers:
                    keeper_dst = os.path.join(self._keeper_directory, os.path.basename(keeper))

                    if os.path.exists(keeper_dst):
                        logger.warning('Keeper name already exists, modifying.')
                        keeper_dst += '_' + generate_nonce()

                    # When binwalk hits a gzip (and likely bz2/xz/etc), with the extract flag it will actually
                    # run the uncompressor on it, thus removing the original compressed file.
                    # This is a simple heuristic for this situation
                    if not os.path.isfile(keeper):

                        # If there is another file, just with the extention removed, let's assume this is the uncompressed version
                        keeper_minus_extension = ".".join(keeper.split(".")[:-1])
                        if keeper_minus_extension in keepers:
                            # This is fine. We may be missing info unfortunately.
                            logger.warning("Looks like binwalk removed this file during extraction %s", keeper)
                            continue

                        logger.warning("Couldn't find extracted file named %s", keeper)
                        continue

                    shutil.move(keeper, keeper_dst)

            os.chdir(saved_dir)

        # TODO: Check if strings of output contain a known word, save if so.

    def _preflight(self):
        """Checks for missing requirements."""

        missing_packages = []

        for package in required_packages:
            if shutil.which(package) is None:
                missing_packages.append(package)

        try:
            import libxmp.utils
        except Exception as e:
            missing_packages.append('libexempi3')

        if missing_packages != []:
            logger.error('Missing the following required packages: ' + ', '.join(missing_packages))
            logger.error('Either install them manually or run \'stegoveritas_install_deps\'.')

    def _parse_args(self, args=None):

        parser = argparse.ArgumentParser(description='Yet another Stego tool',
                                         epilog='Have a good example? Wish it did something more? Submit a ticket: https://github.com/bannsec/stegoVeritas')

        # Core Options
        parser.add_argument('-out', metavar='dir', type=str, help='Directory to place output in. Defaults to ./results', default=os.path.abspath('./results'))
        parser.add_argument('-debug', action='store_true', help='Enable debugging logging.')
        parser.add_argument('-password', type=str, default=None, help='When applicable, attempt to use this password to extract data.')
        parser.add_argument('-wordlist', type=str, default=None, help='When applicable, attempt to brute force with this wordlist.')
        parser.add_argument('file_name', metavar='file', type=str, default=False, help='The file to analyze')

        # Image Options
        image = parser.add_argument_group('image options')
        image.add_argument('-meta', action='store_true', help='Check file for metadata information')
        image.add_argument('-imageTransform', action='store_true', help='Perform various image transformations on the input image and save them to the output directory')
        image.add_argument('-bruteLSB', action='store_true', help='Attempt to brute force any LSB related steganography.')
        image.add_argument('-colorMap', nargs="*", metavar='N', type=int, default=None, help='Analyze a color map. Optional arguments are colormap indexes to save while searching')
        image.add_argument('-colorMapRange', nargs=2, metavar=('Start', 'End'), type=int, default=None, help='Analyze a color map. Same as colorMap but implies a range of colorMap values to keep')
        image.add_argument('-extractLSB', action='store_true', help='Extract a specific LSB RGB from the image. Use with -red, -green, -blue, and -alpha')
        image.add_argument('-red', nargs='+', metavar='index', type=int)
        image.add_argument('-green', nargs='+', metavar='index', type=int)
        image.add_argument('-blue', nargs='+', metavar='index', type=int)
        image.add_argument('-alpha', nargs='+', metavar='index', type=int)
        image.add_argument('-extract_frames', action='store_true', default=False, help='Split up an animated gif into individual frames.')
        image.add_argument('-trailing', action='store_true', help='Check for trailing data on the given file')
        image.add_argument('-steghide', action='store_true', help='Check for StegHide hidden info.')

        # Multi Options
        multi = parser.add_argument_group('multi options')
        multi.add_argument('-exif', action='store_true', default=False, help='Check this file for exif information.')
        multi.add_argument('-xmp', action='store_true', default=False, help='Check this file for XMP information.')
        multi.add_argument('-carve', action='store_true', default=False, help='Attempt to carve/extract things from this file.')

        self.args = parser.parse_args(args)

        if self.args.debug:
            logging.root.setLevel(logging.DEBUG)

        self.file_name = self.args.file_name
        self.results_directory = self.args.out

        # Should this be considered an 'auto' run?
        # TODO: This is SUPER hacky... Should probably find a better way to determine if this is an auto run or not.
        auto = copy(self.args.__dict__)
        auto.pop('out')
        auto.pop('file_name')
        auto.pop('debug')
        self.args.auto = all(option in [False, None, []] for option in auto.values())

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
