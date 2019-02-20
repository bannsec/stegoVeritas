
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_carve_zip_from_elf():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'bin_with_zip_inside'), '-out', tmpdirname, '-carve'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(veritas._keeper_directory))
        found = False
        for f in files:
            with open(os.path.join(veritas._keeper_directory, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'ff22941336956098ae9a564289d1bf1b':
                    found = True
                    break
        assert found == True
