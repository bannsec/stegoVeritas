
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:Meta')

import os
from struct import unpack
import exifread
from .. import png

def run(image):
    """Extracts meta data from the image.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR/metadata
    """

    # This is pretty much replaced entirely by exiftool at the moment..
    return

    args = image.veritas.args

    # Nothing to do
    if not args.auto and not args.meta:
        logger.debug('Nothing to do.')
        return

    if image.file.format == "PNG":
        PNGMeta(image)

    else:
        logger.debug("No metadata parsing support for {0}".format(image.file.format))

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
	# Not sure how to parse these yet...
	if t == "iTXt":
		print(c)
		return ""
	if t == "zTXt":
		print(c)
		return ""
	return ""

def JPEGMeta(image):
    """Deprecated -- This is effectively being replaced by the MultiHandler.Exif."""
    meta = ""

    # Open up the file for reading
    with open(image.veritas.file_name,"rb") as jpegFile:
            tags = exifread.process_file(jpegFile)
            
            for tag in tags:
                    meta += "{0}:\t{1}\n".format(tag,tags[tag])
    
    # Show it to the user	
    print("Exif Data\n=========\n{0}\n".format(meta))
    
    # Save it off
    with open(os.path.join(image.veritas.results_directory,"metadata"),"w") as out:
            out.write(meta)
	

def PNGMeta(image):
	
    r = png.Reader(filename=image.veritas.file_name)
    
    for chunk in r.chunks():
            tmp = parsePNGChunk(chunk[0],chunk[1])
            if tmp != "":
                    print(tmp)

