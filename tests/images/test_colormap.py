
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas
from glob import glob
from stegoveritas.modules.image import SVImage

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_colormap_brute():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap.png'), '-out', tmpdirname, '-colorMap'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            if SVImage.hash_file(os.path.join(tmpdirname, f)) == '6ca611130d0d1ec1298b840fa2461c3015ada2b9ca7831c4dabcdab287abf35c':
                found = True
                break
        assert found == True

        assert len(glob(os.path.join(tmpdirname, '*.png'))) == 256

def test_colormap_extract_index():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap.png'), '-out', tmpdirname, '-colorMap', '1'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            if SVImage.hash_file(os.path.join(tmpdirname, f)) == 'cecc25bfc504053aba9acacfea2037b7ee4512791c8a5a2e9f2e567d8efbb2c2':
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
            if SVImage.hash_file(os.path.join(tmpdirname, f)) == 'cecc25bfc504053aba9acacfea2037b7ee4512791c8a5a2e9f2e567d8efbb2c2':
                found = True
                break
        assert found == True

        # We should see a fully black box (since we are keeping index 1 which will effectively fill in with index 0 to create a full black box)
        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            if SVImage.hash_file(os.path.join(tmpdirname, f)) == '4b2d1eff63d6b494675f20de2ccd13c0103e7c2bf5a0e38474bc6db566f1ee2f':
                found = True
                break
        assert found == True
