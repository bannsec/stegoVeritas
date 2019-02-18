
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_xmp_jpg():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_xmp.jpg'), '-out', tmpdirname, '-xmp'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        xmpdir = os.path.join(tmpdirname, 'xmp')

        assert os.path.isdir(xmpdir)

        _, _, files = next(os.walk(xmpdir))
        found = False
        for f in files:
            with open(os.path.join(xmpdir, f),'r') as f:
                if 'This is some meta information.' in f.read():
                    found = True
                    break

        assert found == True
