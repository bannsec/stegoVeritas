
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:ColorMap')

import os
import numpy
from copy import copy

def run(image):
    """Performs colormap stego extraction.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR
    """

    args = image.veritas.args

    # Nothing to do
    if not args.auto and args.colorMap is None and args.colorMapRange is None:
        logger.debug('Nothing to do.')
        return

    extract_colormap(image)

def extract_colormap(image, saveMap=None):

    bands = image.file.getbands()

    if "P" not in bands:
        logger.debug('Not a colormap. Skipping.')
        return

    if image.veritas.args.colorMap in [[], None]:
        index_to_save = range(0x100)
    else:
        index_to_save = image.veritas.args.colorMap

    if saveMap is None:
        if image.veritas.args.colorMapRange is not None:
            saveMap = range(*image.veritas.args.colorMapRange)
        else:
            saveMap = []

    logger.debug('Extracting colorMap. saveMap={}'.format(saveMap))

    # f.putpalette(f.palette.getdata()[1])
    pal = [255 for x in range(768)]

    for save in saveMap:
            pal[save*3] = 0
            pal[save*3+1] = 0
            pal[save*3+2] = 0
    
    # Break apart the color map to help see things
    #for i in range(0xff + 1):
    for i in index_to_save:
            pal2 = copy(pal)
            pal2[i*3] = 0
            pal2[i*3+1] = 0
            pal2[i*3+2] = 0
            image.file.putpalette(pal2)
            # Change to numpy
            #g = numpy.array(f)
            # Xor our colormap index (keep our save here)
            #g = g ^ (i | saveMap)
            # Contrast
            #g[g != 0] = 0xff
            # Revert to image
            #g = Image.fromarray(g)
            # Save
            image.file.save(os.path.join(image.veritas.results_directory, os.path.basename(image.veritas.file_name) + "_{0}.png".format(i)))
