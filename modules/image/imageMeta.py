import os.path
import sys
from config import SCRIPTDIR
from struct import unpack

sys.path.append(os.path.join(SCRIPTDIR,"modules","image"))

import exifread

def parsePNGChunk(t,c):
	"""
	Input:
		t -- png chunk type
		c -- png chunk of type bytes
	Action:
		Parse the chunk into something human readable
	Returns:
		string containing relevant information
	"""
	out = ""
	
	if t == "IHDR":
		colortype = {
			0: "Gray scale",
			2: "RGB",
			3: "Color and Palette",
			4: "Gray scale + Alpha",
			6: "Color and Alpha Channel"
		}
		compression = {
			0: "Deflate"
		}
		filtering = {
			0: "Adaptive Filtering"
		}
		interlace = {
			0: "No Interlace",
			1: "Adam7 Interlace"
		}
		u = unpack(">IIbbbbb",c)
		out += "{0:<25}: {1}x{2}\n".format("Size",u[0],u[1])
		out += "{1:<25}: {0}\n".format(u[2],"Bit Depth")
		out += "{1:<25}: {0}\n".format(colortype[u[3]],"Color Type")
		out += "{1:<25}: {0}\n".format(compression[u[4]],"Compression Used")
		out += "{1:<25}: {0}\n".format(filtering[u[5]],"Filter Method")
		out += "{1:<25}: {0}".format(interlace[u[6]],"Interlace Method")
		return out
	if t == "PLTE":
		out += "{1:<25}: {0}".format(int(len(c)/3),"Palettes")
		return out
	if t == "IDAT":
		# Not caring about IDAT for the moment
		return ""
	if t == "IEND":
		return ""
	if t == "tEXt":
		c2 = c.split(b"\x00")
		print("{0:<25}: {1}".format(c2[0].decode('iso-8859-1'),c2[1].decode('iso-8859-1')))
	return ""

def JPEGMeta(f,args):
	meta = ""
	
	# Open up the file for reading
	with open(f.filename,"rb") as jpegFile:
		tags = exifread.process_file(jpegFile)
		
		for tag in tags:
			meta += "{0}:\t{1}\n".format(tag,tags[tag])
	
	# Show it to the user	
	print("Exif Data\n=========\n{0}\n".format(meta))
	
	# Save it off
	with open(os.path.join(args.outDir,"metadata"),"w") as out:
		out.write(meta)
	

def PNGMeta(f,args):
	import png
	
	r = png.Reader(filename=f.filename)
	
	for chunk in r.chunks():
		tmp = parsePNGChunk(chunk[0],chunk[1])
		if tmp != "":
			print(tmp)


def auto(f,args):
	"""
	Input:
		f -- PIL Image object
		args -- argparser object
	Action:
		Determine appropriate metadata parser, and parse data
	Returns:
		Nothing
	"""
	
	# JPEG and TIFF Metadata
	if f.format == "JPEG" or f.format == "TIFF":
		JPEGMeta(f,args)
	if f.format == "PNG":
		PNGMeta(f,args)
	else:
		print("No metadata parsing support for {0}".format(f.format))
