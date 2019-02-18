
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_exif_jpg():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_exif_comment.jpg'), '-out', tmpdirname, '-exif'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        exifdir = os.path.join(tmpdirname, 'exif')

        assert os.path.isdir(exifdir)

        _, _, files = next(os.walk(exifdir))
        found = False
        for f in files:
            with open(os.path.join(exifdir, f),'r') as f:
                if 'This is a comment string.' in f.read():
                    found = True
                    break

        assert found == True

def test_exif_png():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_exif.png'), '-out', tmpdirname, '-exif'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        exifdir = os.path.join(tmpdirname, 'exif')

        assert os.path.isdir(exifdir)

        _, _, files = next(os.walk(exifdir))
        found = False
        for f in files:
            with open(os.path.join(exifdir, f),'r') as f:
                if "This is my inserted png chunk." in f.read():
                    found = True
                    break

        assert found == True
