
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_trailing_jpg():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_trailing.jpg'), '-out', tmpdirname, '-trailing'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'be737fc8ea2b8a13ae6420dc4cd09bfa':
                    found = True
                    break
        assert found == True

def test_trailing_tiff():
    # Turns out ffmpeg adds 4 extra '\x00\x00\x00\x00' at the end when converting to tiff. Thus the different md5sum.

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_trailing.tiff'), '-out', tmpdirname, '-trailing'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'df5b9f00a4e15cde88aa8c304033477b':
                    found = True
                    break
        assert found == True

def test_trailing_png():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_trailing.png'), '-out', tmpdirname, '-trailing'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'be737fc8ea2b8a13ae6420dc4cd09bfa':
                    found = True
                    break
        assert found == True

def test_trailing_bmp():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_trailing.bmp'), '-out', tmpdirname, '-trailing'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'be737fc8ea2b8a13ae6420dc4cd09bfa':
                    found = True
                    break
        assert found == True

def test_trailing_gif():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_trailing.gif'), '-out', tmpdirname, '-trailing'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'be737fc8ea2b8a13ae6420dc4cd09bfa':
                    found = True
                    break
        assert found == True
