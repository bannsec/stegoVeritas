
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:Filters')

import os
from PIL import Image, ImageFilter, ImageFile
import numpy
from copy import copy
import multiprocessing

def run_filter(image, f_a, filt):
    try:
        g = f_a.filter(filt)
    except IOError as e:
        # Generically print it, then try again (truncated error)
        logger.error("%s", e)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        g = f_a.filter(filt)

    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_" + filt.name.replace(" ","_") + ".png"))

def run_invert(image, f_a):
    g = numpy.array(f_a)
    g = g ^ 0xff
    g = Image.fromarray(g)
    g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_inverted.png"))

def run_color_planes(image, f_a, plane):

    if plane == "red":
        g = numpy.array(f_a)
        g[:,:,2] *= 0
        g[:,:,1] *= 0
        g = Image.fromarray(g)
        g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_red_plane.png"))
    
    elif plane == "green":
        g = numpy.array(f_a)
        g[:,:,2] *= 0
        g[:,:,0] *= 0
        g = Image.fromarray(g)
        g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_green_plane.png"))

    elif plane == "blue":
        g = numpy.array(f_a)
        g[:,:,0] *= 0
        g[:,:,1] *= 0
        g = Image.fromarray(g)
        g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_blue_plane.png"))

    elif plane == "alpha":
        # TODO: Still assuming all the positions for the given colors in the tuple
        if "A" in image.file.getbands():
                g = numpy.array(image.file)
                g[:,:,0] *= 0
                g[:,:,1] *= 0
                g[:,:,2] *= 0
                g = Image.fromarray(g)
                g.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_alpha_plane.png"))


def run_bit_plane(image, f_a, plane, color, index):
    """Extracts a specific bit plane from the image (i.e.: "Green" bit 0)"""

    temp = numpy.array(plane)
    # Shift over to get right offset
    temp = temp >> index
    # Get the bit
    temp = temp & 1
    # Fix-up the background
    temp[temp == 1] = 255
    # Save it off
    temp = Image.fromarray(temp)
    temp.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_{0}_{1}.png".format(color,index)))

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

    try:
        colorPlanes = image.file.split()
    except OSError as e:
        logger.error("%s", e)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        colorPlanes = image.file.split()

    ###########
    # Filters #
    ###########
    
    # Built-in filters to apply
    filters = [ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.FIND_EDGES, ImageFilter.MaxFilter, ImageFilter.MedianFilter, ImageFilter.MinFilter, ImageFilter.ModeFilter, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.GaussianBlur]
    wait_for = []

    with multiprocessing.Pool() as pool:

        # Generic filters
        for filt in filters:
            wait_for.append(pool.apply_async(run_filter, args=(image, f_a, filt)))

        # Specific color planes
        for plane in ["red", "green", "blue", "alpha"]:
            wait_for.append(pool.apply_async(run_color_planes, args=(image, f_a, plane)))
    
        ##################
        # Bit Map Planes #
        ##################
        
        # TODO: This is an assumption on ordering... Maybe find a better way.
        color = "Red"
        for plane in colorPlanes:
                for i in range(8):
                    # run_bit_plane(image, f_a, color, index
                    wait_for.append(pool.apply_async(run_bit_plane, args=(image, f_a, plane, color, i)))
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

        # Inverting
        wait_for.append(pool.apply_async(run_invert, args=(image, f_a)))

        # Wait for everything to finish
        for w in wait_for: w.wait()
