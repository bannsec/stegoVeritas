
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:BruteLSB')

import os
import shutil
import multiprocessing
from ....helpers import print_error

def run_dump(image, red_index=None, green_index=None, blue_index=None, alpha_index=None):
    logger.debug("Trying red={} green={} blue={} alpha={}".format(red_index, green_index, blue_index, alpha_index))
    o = image.dumpLSBRGBA(red_index=red_index, green_index=green_index, blue_index=blue_index, alpha_index=alpha_index)
    image.veritas.test_output(o)

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

    with multiprocessing.Pool() as pool:
        wait_for = []

        # Try all the same indexes first. More likely stuff up front.
        # i.e.: 0,0,0  1,1,1,  2,2,2
        for i in range(0,8):
            wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'red_index': [i], "green_index": [i], "blue_index": [i]}, error_callback=print_error))

        # Try Red
        i = []
        for x in range(8):
            i.append(x)
            wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'red_index': i[::]}, error_callback=print_error))

        # Try Green
        i = []
        for x in range(8):
            i.append(x)
            wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'green_index': i[::]}, error_callback=print_error))

        # Try Blue
        i = []
        for x in range(8):
            i.append(x)
            wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'blue_index': i[::]}, error_callback=print_error))

        # Try Alpha
        if "A" in image.file.mode:
            i = []
            for x in range(8):
                i.append(x)
                wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'alpha_index': i[::]}, error_callback=print_error))

        # Try across the board
        # i.e.: 0,0,0  01,01,01 etc
        i = []
        for x in range(8):
            i.append(x)
            wait_for.append(pool.apply_async(run_dump, args=(image,), kwds={'red_index': i[::], "green_index": i[::], "blue_index": i[::]}, error_callback=print_error))

        # Wait for everything to finish
        for w in wait_for: w.wait()

    return
    for r in range(0,8):
        for g in range(0,8):
            for b in range(0,8):
                logger.debug("Trying {0}.{1}.{2}".format(r,g,b))
                o = image.dumpLSBRGBA(red_index=[r],green_index=[g],blue_index=[b])
                image.veritas.test_output(o)
