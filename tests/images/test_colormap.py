
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas
from glob import glob

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_colormap_brute():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap.png'), '-out', tmpdirname, '-colorMap'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'dce11a73afc877bf0551d95648f49329':
                    found = True
                    break
        assert found == True

        assert len(glob(os.path.join(tmpdirname, '*'))) == 256

def test_colormap_extract_index():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap.png'), '-out', tmpdirname, '-colorMap', '1'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'e8acfd2023de5ec5f111dc64c30f9541':
                    found = True
                    break
        assert found == True

def test_colormap_extract_range_keep():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap.png'), '-out', tmpdirname, '-colorMapRange', '1', '2'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        # We should see our secret text
        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == 'e8acfd2023de5ec5f111dc64c30f9541':
                    found = True
                    break
        assert found == True

        # We should see a fully black box (since we are keeping index 1 which will effectively fill in with index 0 to create a full black box)
        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == '6fbafc23c7ae20d14bcd6b892a849f39':
                    found = True
                    break
        assert found == True
