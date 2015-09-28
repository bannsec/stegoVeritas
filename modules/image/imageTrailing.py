import os.path
from struct import unpack

# Look for trailing data in images

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
	steg = open(f.filename,"rb").read()
	
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
	else:
		print("Image Trailing: No support yet for format {0}".format(f.format))
		return
