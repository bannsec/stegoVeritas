
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:BruteLSB')

import os
import shutil

def run(image):
    """Attempts to brute force out any LSB stego.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR
    """

    args = image.veritas.args

    # Nothing to do
    if not args.auto and not args.bruteLSB:
        logger.debug('Nothing to do.')
        return

    if image.file.mode == "P":
        logger.debug('Image is colormap, skipping..')
        return

    # Try all the same indexes first. More likely stuff up front.
    # i.e.: 0,0,0  1,1,1,  2,2,2
    for i in range(0,8):
        logger.debug("Trying {0}.{0}.{0}".format(i))
        o = image.dumpLSBRGBA(red_index=[i],green_index=[i],blue_index=[i])
        image.veritas.test_output(o)

    # Try Red
    i = []
    for x in range(8):
        i.append(x)
        logger.debug("Trying Red {0}".format(i))
        o = image.dumpLSBRGBA(red_index=i)
        image.veritas.test_output(o)

    # Try Green
    i = []
    for x in range(8):
        i.append(x)
        logger.debug("Trying Green {0}".format(i))
        o = image.dumpLSBRGBA(green_index=i)
        image.veritas.test_output(o)

    # Try Blue
    i = []
    for x in range(8):
        i.append(x)
        logger.debug("Trying Blue {0}".format(i))
        o = image.dumpLSBRGBA(blue_index=i)
        image.veritas.test_output(o)

    # Try Alpha
    if "A" in image.file.mode:
        i = []
        for x in range(8):
            i.append(x)
            logger.debug("Trying Alpha {0}".format(i))
            o = image.dumpLSBRGBA(alpha_index=i)
            image.veritas.test_output(o)

    # Try across the board
    # i.e.: 0,0,0  01,01,01 etc
    i = []
    for x in range(8):
        i.append(x)
        logger.debug("Trying {0}x{0}x{0}".format(i))
        o = image.dumpLSBRGBA(red_index=i,green_index=i,blue_index=i)
        image.veritas.test_output(o)

    return
    for r in range(0,8):
        for g in range(0,8):
            for b in range(0,8):
                logger.debug("Trying {0}.{1}.{2}".format(r,g,b))
                o = image.dumpLSBRGBA(red_index=[r],green_index=[g],blue_index=[b])
                image.veritas.test_output(o)
