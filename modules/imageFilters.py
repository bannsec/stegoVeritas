from PIL import Image,ImageFilter
import os
import numpy

# Take input PIL.Image file and perform many filters on it

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



