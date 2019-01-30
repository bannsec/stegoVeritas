
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:ExtractLSB')


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

    o = image.dumpLSBRGBA(f=f,rIndex=r,gIndex=g,bIndex=b,aIndex=a)
    f = open(os.path.join(args.outDir,"LSBExtracted.bin"),"wb")
    f.write(o)
    f.close()

    print("Extracted to {0}".format(os.path.join(args.outDir,"LSBExtracted.bin")))
    return
