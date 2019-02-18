
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas
from glob import glob
from stegoveritas.modules.image import SVImage

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_extract_frames_gif():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'colormap_stego.gif'), '-out', tmpdirname, '-extract_frames'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        frames = glob(os.path.join(tmpdirname, '*_frame_*.gif'))

        assert len(frames) == 3

        expected_hashes = ['9b20f6b8452dcae537a3f22fc7dc6ba6a6ee9515ba4cdb336b4b9bf0b315585b', '0b62f28193c2cc87491b64bf87e8ed766563e0fd0bacaf8fecca518dcd92c40e', '6f49579ae11418d8cd81034cb3259c454d798494bade011829ad39c9416e6ccf']

        for f in frames:
            assert SVImage.hash_file(os.path.join(tmpdirname, f)) in expected_hashes
