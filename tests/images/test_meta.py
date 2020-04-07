
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_meta_exif():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_exif1.jpg'), '-out', tmpdirname, '-exif'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        with open(os.path.join(tmpdirname, "exif", "description"), "rb") as f:
            assert b"Alabama defensive back Xavier McKinney" in f.read()

        """
        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'be737fc8ea2b8a13ae6420dc4cd09bfa':
                    found = True
                    break
        assert found == True
        """
