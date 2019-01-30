
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:ExtractLSB')

import os


def run(image):
    """Extracts byte stream of Least Significant Bits.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR/LSBExtracted.bin
    """

    args = image.veritas.args

    # Nothing to do
    if not args.extractLSB:
        logger.debug('Nothing to do.')
        return

    if args.red:
            r = args.red
    else:
            r = []

    if args.green:
            g = args.green
    else:
            g = []

    if args.blue:
            b = args.blue
    else:
            b = []

    if args.alpha:
            a = args.alpha
    else:
            a = []

    print("Extracting ({0},{1},{2},{3})".format(r,g,b,a))

    extract_location = os.path.join(image.veritas.results_directory,"LSBExtracted.bin")
    o = image.dumpLSBRGBA(red_index=r,green_index=g,blue_index=b,alpha_index=a)
    with open(extract_location,"wb") as f:
        f.write(o)

    print("Extracted to {0}".format(extract_location))
