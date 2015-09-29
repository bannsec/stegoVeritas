import os.path
from struct import unpack

# Look for trailing data in images

def tiff(f,args):
	"""
	Input:
		f -- PIL Image file
		args -- arg parsed arguments
	Action:
		Checks for trailing information in file. Print and save if found.
	Returns:
		Nothing
	"""
	
	# Read in the file
	with open(f.filename,"rb") as myFile:
		steg = myFile.read()
	
	# Parse magic
	if steg[0:4] == b"II*\x00":
		fmt = "<I"
		fmt_s = "<h"
	elif steg[0:4] == b"MM*\x00":
		fmt = ">I"
		fmt_s = ">h"
	else:
		print("Trailing: Error Invalid tiff magic numbers")
		return
	
	# Read header
	ifd = unpack(fmt,steg[4:8])[0]
	
	# Read the number of tags
	nEntries = unpack(fmt_s,steg[ifd:ifd+2])[0]
	
	# We want to find the maximum address
	# Right now our max address is the end of the IFD block
	maxAddr = ifd + (nEntries*0xc) + 2
	
	# Loop through the tags
	for i in range(nEntries):
		# Figure out our current file location
		curAddr = ifd + 2 + (i * 0xc)

		tag = unpack(fmt_s,steg[curAddr:curAddr+2])[0]
		tagType = unpack(fmt_s,steg[curAddr+2:curAddr+4])[0]
		count = unpack(fmt,steg[curAddr+4:curAddr+8])[0]
		
		# print("Tag: {0}\nType: {1}".format(tag,tagType))

		# Tag types of ASCII and Unknown both have offsets associated
		if tagType == 2 or tagType == 7:
			offset = unpack(fmt,steg[curAddr+8:curAddr+0xc])[0]
			# See if we have a new winner
			if (offset + count) > maxAddr:
				maxAddr = offset + count
				#print("New max offset")
			# print("Found new offset: {0}".format(hex(offset)))

	# See if we have data hiding at the end
	if len(steg) > maxAddr:
		print("Trailing Data Discovered... Saving")
		print(steg[maxAddr:])
		with open(os.path.join(args.outDir,"trailing_data.bin"),"wb") as outFile:
			outFile.write(steg[maxAddr:])


def jpeg(f,args):
	"""
	Input:
		f -- PIL Image file
		args -- arg parsed arguments
	Action:
		Checks for trailing information in file. Print and save if found.
	Returns:
		Nothing
	"""

	# Official specs here: http://www.w3.org/Graphics/JPEG/itu-t81.pdf	

	# Index for marching through the file	
	i = 0
	
	# These markers don't have a length attribute
	nonLenMarkers = [ b'\xff\xd8', b'\xff\x01', b'\xffd0', b'\xffd1', b'\xffd2', b'\xffd3', b'\xffd4', b'\xffd5', b'\xffd6', b'\xffd7' ]

	# Open up the file
	with open(f.filename,"rb") as myFile:
		steg = myFile.read()
	
	while True:
		# Grab the current header
		hdr = steg[i:i+2]
		
		# TODO: Add py logging here
		#print("Found Header: {0}".format(hdr))
		
		# if Start of Image, Temporary Private, Restart, things that don't have an associated length field
		if hdr in nonLenMarkers:
			# Just move to the next marker
			i = i + 2
			continue
		
		# If we've found our way to the end of the jpeg
		if hdr == b'\xff\xd9':
			#print("Made it to the end!")
			# Increment 2 so we can check the length
			i += 2
			break
		
		# Unpack the length field
		ln = unpack(">H",steg[i+2:i+4])[0]
		
		# print("Found Length: {0}".format(ln))
		
		# Update the index with the known length
		i = i+ln+2
		
		# When we hit scan data, we scan to the end of the format
		if hdr == b'\xff\xda':
			#print("Start of Scan data")
			# Find the end marker
			i += steg[i:].index(b'\xff\xd9')
	
	# Check for trailers
	if i != len(steg):
		print("Trailing Data Discovered... Saving")
		print(steg[i:])
		# Save it off for reference
		with open(os.path.join(args.outDir,"trailing_data.bin"),"wb") as outFile:
			outFile.write(steg[i:])

def auto(f,args):
	"""
	Input:
		f -- PIL Image file
		args -- arg parsed arguments
	Action:
		Based on file type, checks for trailing information in file. Print and save if found.
	Returns:
		Nothing
	"""
	
	if f.format == "JPEG":
		jpeg(f,args)
		return
	elif f.format == "TIFF":
		tiff(f,args)
		return
	else:
		print("Image Trailing: No support yet for format {0}".format(f.format))
		return
