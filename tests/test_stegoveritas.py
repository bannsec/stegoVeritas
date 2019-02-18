
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_test_output_binwalk():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'images', 'owl_trailing.jpg'), '-out', tmpdirname]
        veritas = stegoveritas.StegoVeritas(args=args)

        with open(veritas.file_name, 'rb') as f:
            data = f.read()

        veritas.test_output(data)

        _, _, files = next(os.walk(veritas._keeper_directory))
        found = False
        for f in files:
            with open(os.path.join(veritas._keeper_directory, f),'rb') as f:
                # text.txt
                if hashlib.md5(f.read()).hexdigest() == 'ff22941336956098ae9a564289d1bf1b':
                    found = True
                    break
        assert found == True

