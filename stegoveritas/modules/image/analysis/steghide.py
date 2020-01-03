
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:StegHide')

import os
import hashlib
import random
import subprocess

def run(image):
    """Attempts to extract steghide based stego.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR/steghide.bin
    """

    global output_file
    output_file = os.path.join(image.veritas.results_directory, "steghide.bin")

    args = image.veritas.args

    # Nothing to do
    if not args.auto and not args.steghide:
        logger.debug('Nothing to do.')
        return

    # Always try without password
    try_extract(image)

    # Try password
    if args.password is not None:
        try_extract(image, args.password)

    # Brute force wordlist
    if args.wordlist is not None:

        with open(args.wordlist, "r") as f:
            line = f.readline().strip()

            while line:
                try_extract(image, line)
                line = f.readline().strip()

def try_extract(image, password=None):

    nonce = hashlib.md5(str(random.random()).encode()).hexdigest()
    outfile = os.path.join(image.veritas.results_directory, "steghide_" + nonce + ".bin")

    try:

        subprocess.check_output(["steghide", "extract", "-sf", image.veritas.file_name, "-xf", outfile, "-p", password or ""], stderr=subprocess.PIPE)
        print("Found something with StegHide: " + outfile)

    except:
        pass

