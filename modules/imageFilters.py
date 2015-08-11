from PIL import Image,ImageFilter
import os
import numpy
from copy import copy

# Take input PIL.Image file and perform many filters on it

def colorMap(f,outDir,saveMap = []):
	"""
	Take care of the colormaps
	"""
	fileName = f.filename	

	# f.putpalette(f.palette.getdata()[1])
	pal = [255 for x in range(768)]

	for save in saveMap:
		pal[save*3] = 0
		pal[save*3+1] = 0
		pal[save*3+2] = 0
	
	# Break apart the color map to help see things
	for i in range(0xff + 1):
		pal2 = copy(pal)
		pal2[i*3] = 0
		pal2[i*3+1] = 0
		pal2[i*3+2] = 0
		f.putpalette(pal2)
		# Change to numpy
		#g = numpy.array(f)
		# Xor our colormap index (keep our save here)
		#g = g ^ (i | saveMap)
		# Contrast
		#g[g != 0] = 0xff
		# Revert to image
		#g = Image.fromarray(g)
		# Save
		f.save(os.path.join(outDir,fileName + "_{0}.png".format(i)))
	
	

def run(f,outDir):
	"""
	Input:
		f == PIL.Image class
		outDir == location to save to (i.e.: /tmp)
	Action:
		Run a bunch of filters, modifications, and transformations on f and save them
	Returns:
		Nothing. Images are saved into outDir
	"""
	# Save the filename
	fileName = f.filename
	
	# Set alpha if it exists.. f_a == the same image but with the alpha layer full
	bands = f.getbands()
	if "A" in bands:
		index = bands.index("A")
		f_a = numpy.array(f)
		f_a[:,:,index] = 0xff
		f_a = Image.fromarray(f_a)
	# Using an else here to keep things simple. If you use f_a you will always have a working non-alpha image
	else:
		f_a = f

	# Check what type of image is it
	# ColorMap
	if "P" in bands:
		print("Colormap detected...")
		colorMap(f,outDir)
		return

	###########
	# Filters #
	###########
	
	# Built-in filters to apply
	filters = [ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.FIND_EDGES, ImageFilter.MaxFilter, ImageFilter.MedianFilter, ImageFilter.MinFilter, ImageFilter.ModeFilter, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.GaussianBlur]
	
	for filt in filters:
		g = f_a.filter(filt)
		g.save(os.path.join(outDir,fileName + "_" + filt.name.replace(" ","_") + ".png"))
	
	################
	# Color planes #
	################
	g = numpy.array(f_a)
	g[:,:,2] *= 0
	g[:,:,1] *= 0
	g = Image.fromarray(g)
	g.save(os.path.join(outDir,fileName + "_red_plane.png"))
	
	g = numpy.array(f_a)
	g[:,:,2] *= 0
	g[:,:,0] *= 0
	g = Image.fromarray(g)
	g.save(os.path.join(outDir,fileName + "_green_plane.png"))

	g = numpy.array(f_a)
	g[:,:,0] *= 0
	g[:,:,1] *= 0
	g = Image.fromarray(g)
	g.save(os.path.join(outDir,fileName + "_blue_plane.png"))

	# TODO: Still assuming all the positions for the given colors in the tuple
	if "A" in bands:
		g = numpy.array(f)
		g[:,:,0] *= 0
		g[:,:,1] *= 0
		g[:,:,2] *= 0
		g = Image.fromarray(g)
		g.save(os.path.join(outDir,fileName + "_alpha_plane.png"))

	
	##################
	# Bit Map Planes #
	##################
	colorPlanes = f.split()
	
	# TODO: This is an assumption on ordering... Maybe find a better way.
	color = "Red"
	for plane in colorPlanes:
		for i in range(8):
			temp = numpy.array(plane)
			# Shift over to get right offset
			temp = temp >> i
			# Get the bit
			temp = temp & 1
			# Fix-up the background
			temp[temp == 1] = 255
			# Save it off
			temp = Image.fromarray(temp)
			temp.save(os.path.join(outDir,fileName + "_{0}_{1}.png".format(color,i)))
		# Move to next color
		if color == "Red":
			color = "Green"
		elif color == "Green":
			color = "Blue"
		elif color == "Blue":
			color = "Alpha"
		elif color == "Alpha":
			color = "Error"
		else:
			raise Exception("We got more planes than we were expecting...\nPlanes: {0}".format(colorPlanes))

	##########
	# Invert #
	##########
	g = numpy.array(f_a)
	g = g ^ 0xff
	g = Image.fromarray(g)
	g.save(os.path.join(outDir,fileName + "_inverted.png"))



