
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_extract_red():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'lsb_red_0.png'), '-out', tmpdirname, '-extractLSB', '-red', '0'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        # Verify we're expecting that
        with open(os.path.join(tmpdirname, 'LSBExtracted.bin'),'rb') as f:
            assert hashlib.md5(f.read()).hexdigest() == '20ba8aa2da066e371747502079991071'

# TODO: Extract blue, green, and combination

test_extract_red()
