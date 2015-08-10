#!/usr/bin/python3

from PIL import Image
import subprocess
import binascii
import os, os.path
import time
import shutil

# Get our current dir
CWD = os.path.dirname(os.path.realpath(__file__))

TEMPFILE = os.path.join(CWD,"stegodone.temp")
# TODO: Use python to make this dynamic
RESULTSDIR = os.path.join(CWD,"results")

# Load the image
f = Image.open("blind")

def _dumpLSB(img,index):
	"""
	Input:
		img == PIL image (type PIL.Image.Image)
		index == integer from LSB to extract (0 == first bit, 1 == second bit, etc)
	Action:
		Extract array of bits represented as integers
	Returns:
		Bit integer array (i.e.: [0,1,1,0,0,1,0,1 ...]
	"""
	# Make sure we're working with the right thing
	if type(img) != Image.Image:
		raise Exception("_dumpLSB: image type should be PIL.Image.Image.\nActual image type is {0}".format(type(img))) 
	
	# Check index
	if index >= 8:
		raise Exception("_dumpLSB: index cannot be >= 8.\nActual index is {0}".format(index))
	
	# Perform bit extraction
	out = [str((byte >> index) & 1) for byte in img.tobytes()]
	
	return out

# Change this to a primitive to dump any given index of a given color
# Then, handle the weaving of those together in a different function
def _dumpLSBRGBA(rIndex = None,gIndex = None,bIndex = None,aIndex = None):
	"""
	Input: 
		rIndex, gIndex, bIndex, aIndex as array of integer indexes (up to 8) to dump
		ex: [0],None,None would dump only the least significant bit of the Red field
	Action:
		Creates a byte array containing the output of the LSB dump (RGBA order) requested
		If needed, it will use the least significant bit first, then bit plane order of red->green->blue->alpha
	Returns:
		Byte array of the result of the action
		ex: b'\x01\x02\x03\x04' etc
	"""
	print("First")
	# Split the file into parts
	r,g,b = f.split()
	
	# Init the dicts
	rDict = {}
	gDict = {}
	bDict = {}
	aDict = {}
	
	#############
	# Red Stuff #
	#############
	if rIndex != None:
		for index in rIndex:
			rDict[index] = _dumpLSB(r,index)
	

	################
	# Greeen Stuff #
	################
	if gIndex != None:
		for index in gIndex:
			gDict[index] = _dumpLSB(g,index)

	##############
	# Blue Stuff #
	##############
	if bIndex != None:
		for index in bIndex:
			bDict[index] = _dumpLSB(b,index)
	
	###############
	# Alpha Stuff #
	###############
	if aIndex != None:
		for index in aIndex:
			aDict[index] = _dumpLSB(a,index)
	
	# Find the first byte for each pixel
	#binStr2 = ''.join([str(byte & 1) for byte in r.tobytes()])
	
	
	##################
	# Combine Output #
	##################
	print("Second")
	# We'll be keeping the binary string here
	binStr = ''

	# Figure out valid index ranges
	indexes = list(set((list(rDict.keys()) + list(gDict.keys()) + list(bDict.keys()))))
	indexes.sort()

	# Loop through all the bytes of the image
	for bit in range(0,f.size[0] * f.size[1]):
		# Loop through all the possible desired indexes
		for index in indexes:
			# If this is a value we're extracting
			if rIndex != None and index in rDict:
				binStr += rDict[index][bit]
			if gIndex != None and index in gDict:
				binStr += gDict[index][bit]
			if bIndex != None and index in bDict:
				binStr += bDict[index][bit]
			if aIndex != None and index in aDict:
				binstr += aDict[index][bit]
	
	print("Third")	
	# Parse those into bytes
	bArray = []
	for i in range(0,len(binStr),8):
		bArray.append(int(binStr[i:i+8],2))
	print("Fourth")	
	# Change bytes into a bit array for writing
	bits = ''.join([chr(b) for b in bArray]).encode('iso-8859-1')
	print("Fifth")	
	return bits

def testOutput(b):
	"""
	Input:
		b = byte array output, generally from the dump functions
		ex: b = b'\x01\x02\x03'
	Action:
		Test if output is worth keeping.
		Initially, this is using the Unix file command on the output and checking for non "Data" returns
	Return:
		Nothing. Move output into keep directory if it's worth-while	
	"""

	# Write out the buffer	
	temp = open(TEMPFILE,"wb")
	temp.write(b)
	temp.close()
	
	# Run the file command
	out = subprocess.check_output(["file",TEMPFILE])
	
	# We like anything that's not just data
	if b': data\n' not in out:
		print("Found something worth keeping!\n{0}".format(out))
		shutil.move(TEMPFILE,os.path.join(RESULTSDIR,str(time.time())))

	try:
		# Remove our mess
		os.unlink(TEMPFILE)
	except OSError:
		pass


for r in range(0,3):
	for g in range(0,3):
		for b in range(0,3):
			print("Trying {0}.{1}.{2}".format(r,g,b))
			o = _dumpLSBRGBA(rIndex=[r],gIndex=[g],bIndex=[b])
			testOutput(o)


# m = magic.Magic(magic.MAGIC_MIME)
# subprocess.check_output(["file","CoolPic.png"])
# subprocess.check_output("file *",shell=True)

# find . -maxdepth 1 -type f -exec binwalk -eM {} \;

