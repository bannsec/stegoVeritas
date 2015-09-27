#!/usr/bin/python3

# TODO: Implement multi-threading pool: https://docs.python.org/3/library/concurrent.futures.html

from PIL import Image
import binascii
import os, os.path
import argparse
from config import *

# Make the folder if need be
os.makedirs(RESULTSDIR,exist_ok=True)

def openFile(fileName):
	"""
	Input:
		fileName == name of file to open
	Action:
		Attempt to open fileName in various ways to determine proper handler
	Returns:
		(fType,[f]) where fType is in ["Image"], and [f] contains the details of the opened file
		The values returned here will be dependent on the type of file identified
	"""
	
	try:
		f = Image.open(fileName)
		return ("Image",[f])
	except:
		print("Error: Unknown or unsupported file type")
		exit(1)


def printFileInformation(fType,x):
	if fType == "Image":
		x = x[0]
		print("Type:\t{0}".format(x.format_description))
		print("Mode:\t{0}\n".format("ColorMap" if x.mode == "P" else x.mode))
		return
	else:
		print("Error... Cannot determine file type")
		return

# Get the commandline input
parser = argparse.ArgumentParser(description='Yet another Stego tool')
parser.add_argument('fileName',metavar='file',type=str,nargs=1,help='The file to analyze')
parser.add_argument('-outDir',metavar='dir',type=str,nargs=1,help='Directory to place output in. Defaults to ./results',default=[RESULTSDIR])
#parser.add_argument('-auto',action='store_true',help='Automatically perform analysis on the file given.')
parser.add_argument('-imageTransform',action='store_true',help='Perform various image transformations on the input image and save them to the output directory')
parser.add_argument('-bruteLSB',action='store_true',help='Attempt to brute force any LSB related stegonography.')
parser.add_argument('-colorMap',nargs="*",metavar='N',type=int,help='Analyze a color map. Optional arguments are colormap indexes to save while searching')
parser.add_argument('-colorMapRange',nargs=2,metavar=('Start','End'),type=int,help='Analyze a color map. Same as colorMap but implies a range of colorMap values to keep')
parser.add_argument('-extractLSB',action='store_true',help='Extract a specific LSB RGB from the image. Use with -red, -green, -blue, and -alpha')
parser.add_argument('-red',nargs='+',metavar='index',type=int)
parser.add_argument('-green',nargs='+',metavar='index',type=int)
parser.add_argument('-blue',nargs='+',metavar='index',type=int)
parser.add_argument('-alpha',nargs='+',metavar='index',type=int)

args = parser.parse_args()
fileName = args.fileName[0]

fType,fArray = openFile(fileName)

printFileInformation(fType,fArray)
args.outDir = args.outDir[0]

if fType == "Image":
	import modules.image
	modules.image.run(fArray,args)


exit(0)


if args.imageTransform:
	import modules.imageFilters as imageFilters
	imageFilters.run(f,RESULTSDIR)


#o = _dumpLSBRGBA(bIndex=[1,2,3],gIndex=[1],aIndex=[0])
#print(o)
#exit()

# m = magic.Magic(magic.MAGIC_MIME)
# subprocess.check_output(["file","CoolPic.png"])
# subprocess.check_output("file *",shell=True)

# find . -maxdepth 1 -type f -exec binwalk -eM {} \;

