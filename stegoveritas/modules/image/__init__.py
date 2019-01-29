
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image')

import os.path
import sys
from PIL import Image

from .. import ModuleBase

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


    def run(self):
        print('Passing on this.')
        pass
    
    @property
    def file(self):
        """PIL Image Instantiation."""
        return self.__file

    @file.setter
    def file(self, file):
        self.__file = file

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
	
	

def extractLSB(f,args):
	"""
	Input:
		args -- The parsed list of program arguments
	Action:
		Extract LSB for given arguments. Save to RESULTSDIR/LSBExtracted.bin
	Returns:
		Nothing
	"""
	if args.red:
		r = args.red
	else:
		r = []
	if args.green:
		g = args.green
	else:
		g = []
	if args.blue:
		b = args.blue
	else:
		b = []
	if args.alpha:
		a = args.alpha
	else:
		a = []

	print("Extracting ({0},{1},{2},{3})".format(r,g,b,a))

	o = modules.image.imageLSB._dumpLSBRGBA(f=f,rIndex=r,gIndex=g,bIndex=b,aIndex=a)
	f = open(os.path.join(args.outDir,"LSBExtracted.bin"),"wb")
	f.write(o)
	f.close()

	print("Extracted to {0}".format(os.path.join(args.outDir,"LSBExtracted.bin")))
	return


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
