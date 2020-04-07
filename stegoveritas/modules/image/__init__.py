
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image')

import os
import sys
from PIL import Image, ImageFile
from prettytable import PrettyTable

from .. import ModuleBase
import hashlib

class SVImage(ModuleBase):

    def __init__(self, veritas):
        super().__init__(veritas)

        # Can we handle this file?
        try:
            self.file = Image.open(veritas.file_name)
            self.valid = True

        except:
            self.valid = False
            logger.info('Cannot handle this file type.')
            return
        
    # Change this to a primitive to dump any given index of a given color
    # Then, handle the weaving of those together in a different function
    def dumpLSBRGBA(self, red_index=None, green_index=None, blue_index=None,
            alpha_index = None):
        """
        Input: 
                red_index, green_index, blue_index, alpha_index as array of integer indexes (up to 8) to dump
                ex: [0],None,None would dump only the least significant bit of the Red field
        Action:
                Creates a byte array containing the output of the LSB dump (RGBA order) requested
                If needed, it will use the least significant bit first, then bit plane order of red->green->blue->alpha
        Returns:
                Byte array of the result of the action
                ex: b'\x01\x02\x03\x04' etc
        """

        if red_index is None: red_index = []
        if green_index is None: green_index = []
        if blue_index is None: blue_index = []
        if alpha_index is None: alpha_index = []

        ##################
        # Combine Output #
        ##################
        # We'll be keeping the binary string here
        binStr = ''

        # Figure out valid index ranges
        indexes = list(set(red_index + green_index + blue_index + alpha_index))
        indexes.sort()

        # Figure out what we have to work with
        bands = self.file.getbands()

        # Get the image bytes
        try:
            fBytes = self.file.tobytes()
        except IOError as e:
            # Generically print it, then try again (truncated error)
            logger.error("%s", e)
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            fBytes = self.file.tobytes()

        # TODO: The following assumes an ordering of RGBA. If this is ever not the case, things will get mixed up
        # Loop through all the bytes of the image
        for byte in range(0,self.file.size[0] * self.file.size[1] * len(bands),len(bands)):
                # Loop through all the possible desired indexes
                for index in indexes:
                        # If this is a value we're extracting
                        if index in red_index:
                                binStr += str(fBytes[byte + 0] >> index & 1)
                        if index in green_index:
                                binStr += str(fBytes[byte + 1] >> index & 1)
                        if index in blue_index:
                                binStr += str(fBytes[byte + 2] >> index & 1)
                        if index in alpha_index:
                                binStr += str(fBytes[byte + 3] >> index & 1)

        # Parse those into bytes
        bArray = []
        for i in range(0,len(binStr),8):
                bArray.append(int(binStr[i:i+8],2))

        # Change bytes into a bit array for writing
        bits = ''.join([chr(b) for b in bArray]).encode('iso-8859-1')

        return bits

    @staticmethod
    def hash_file(file_name):
        """Custom image file hasing algorithm in an attempt to make hashing less brittle to meta information.

        Args:
            file_name (str): String path to file
    
        Returns:
            bytes: Hash of the given file.
        """
        
        img = Image.open(file_name)
        f = img.tobytes()
        
        # Need to account for the palette
        if img.mode == 'P':
            f += img.palette.mode.encode()
            f += img.palette.palette

        img.close()
        return hashlib.sha256(f).hexdigest()
            
    
    @property
    def file(self):
        """PIL Image Instantiation."""
        return self.__file

    @file.setter
    def file(self, file):
        self.__file = file

    @property
    def description(self):
        table = PrettyTable(['Image Format', 'Mode'])
        table.add_row([self.file.format_description, 'ColorMap' if self.file.mode == 'P' else self.file.mode])
        return str(table)


def autoAnalysis(f,args):
	"""
	Input:
		f -- PIL file Image object
		args -- argument array as parsed by argparse
	Action:
		Perform a default set of analysis on the image
	Returns:
		Nothing
	"""
	
	# Check metadata
	print("Checking Meta Data\n")
	modules.image.imageMeta.auto(f,args)	
	
	# Check for trailing data
	print("Checking for trailing data")
	modules.image.imageTrailing.auto(f,args)
	
	# Run the filers on it
	print("Running image filters")
	modules.image.imageFilters.auto(f,args.outDir)

	if f.mode == "P":
		print("Image is a colormap, skipping LSB Extract")
		return

	# Brute LSB
	print("Attempting to brute force LSB items")
	modules.image.imageLSB.auto(f,args)
	
	
def run(fArray,args):
	"""
	Primary handler for Image type stego
	Input:
		fArray is the array returned by the previous open call. In this case it should be a PIL image object
		args is the array parsed by the main program and contains what arguments were passed to the program
	Action:
		Runs analysis on the Image, prompting the user if necessary
	Returns:
		Nothing
	"""
	
	# Grab the file object
	f = fArray[0]
	
	# Determine if we're dealing with the Alpha band
	hasAlpha = "A" in f.getbands()

	# Check for the default case
	if len(sys.argv) == 2:
		autoAnalysis(f,args)
		return

	# Check for action based on flags	
	if args.extractLSB:
		extractLSB(f,args)

	if args.bruteLSB:
		modules.image.imageLSB.auto(f,args)

	if args.colorMapRange != None:
		args.colorMap = range(args.colorMapRange[0],args.colorMapRange[1]+1)

	if args.colorMap != None:
		modules.image.imageFilters.colorMap(f,args.outDir,args.colorMap)
	
	if args.imageTransform:
		modules.image.imageFilters.auto(f,args.outDir)
	
	if args.meta:
		modules.image.imageMeta.auto(f,args)

	if args.trailing:
		modules.image.imageTrailing.auto(f,args)

#from . import imageLSB, imageFilters, imageMeta, imageTrailing
