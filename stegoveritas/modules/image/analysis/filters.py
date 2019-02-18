
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:Filters')

import os
from PIL import Image,ImageFilter
import numpy
from copy import copy

def run(image):
    """Performs various graphical filters on the image.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR
    """

    args = image.veritas.args

    # Nothing to do
    if not args.auto and not args.imageTransform:
        logger.debug('Nothing to do.')
        return

    # Set alpha if it exists.. f_a == the same image but with the alpha layer full
    bands = image.file.getbands()
    if "A" in bands:
            index = bands.index("A")
            f_a = numpy.array(image.file)
            f_a[:,:,index] = 0xff
            f_a = Image.fromarray(f_a)
    # Using an else here to keep things simple. If you use f_a you will always have a working non-alpha image
    else:
            f_a = image.file

    # Check what type of image is it
    # ColorMap
    if "P" in bands:
        logger.debug('Image is colormap, skipping.')
        return

    ###########
    # Filters #
    ###########
    
    # Built-in filters to apply
    filters = [ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.FIND_EDGES, ImageFilter.MaxFilter, ImageFilter.MedianFilter, ImageFilter.MinFilter, ImageFilter.ModeFilter, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.GaussianBlur]
    
    for filt in filters:
            g = f_a.filter(filt)
            g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_" + filt.name.replace(" ","_") + ".png"))
    
    ################
    # Color planes #
    ################
    g = numpy.array(f_a)
    g[:,:,2] *= 0
    g[:,:,1] *= 0
    g = Image.fromarray(g)
    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_red_plane.png"))
    
    g = numpy.array(f_a)
    g[:,:,2] *= 0
    g[:,:,0] *= 0
    g = Image.fromarray(g)
    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_green_plane.png"))

    g = numpy.array(f_a)
    g[:,:,0] *= 0
    g[:,:,1] *= 0
    g = Image.fromarray(g)
    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_blue_plane.png"))

    # TODO: Still assuming all the positions for the given colors in the tuple
    if "A" in bands:
            g = numpy.array(image.file)
            g[:,:,0] *= 0
            g[:,:,1] *= 0
            g[:,:,2] *= 0
            g = Image.fromarray(g)
            g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_alpha_plane.png"))

    
    ##################
    # Bit Map Planes #
    ##################
    colorPlanes = image.file.split()
    
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
                    temp.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_{0}_{1}.png".format(color,i)))
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
    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_inverted.png"))



