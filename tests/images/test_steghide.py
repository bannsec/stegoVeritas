
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import stegoveritas
from glob import glob
from stegoveritas.modules.image import SVImage

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_steghide_nopass():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_steghide_nopass.jpg'), '-out', tmpdirname, '-steghide'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        hidden = glob(os.path.join(tmpdirname, 'steghide_*.bin'))

        assert len(hidden) == 1

        with open(os.path.join(tmpdirname, hidden[0]), "r") as f:
            assert f.read().startswith("This is hidden!")

def test_steghide_password():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_steghide_password.jpg'), '-out', tmpdirname, '-steghide', '-password', 'ThisIsThePassword'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        hidden = glob(os.path.join(tmpdirname, 'steghide_*.bin'))

        assert len(hidden) == 1

        with open(os.path.join(tmpdirname, hidden[0]), "r") as f:
            assert f.read().startswith("This is hidden!")

def test_steghide_wrong_password():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_steghide_password.jpg'), '-out', tmpdirname, '-steghide', '-password', 'ThisIsNotThePassword'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        hidden = glob(os.path.join(tmpdirname, 'steghide_*.bin'))

        assert len(hidden) == 0

def test_steghide_wordlist():

    wordlist = os.path.join(SCRIPTDIR, 'wordlist.txt')

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_steghide_password.jpg'), '-out', tmpdirname, '-steghide', '-wordlist', wordlist] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        hidden = glob(os.path.join(tmpdirname, 'steghide_*.bin'))

        assert len(hidden) == 1

        with open(os.path.join(tmpdirname, hidden[0]), "r") as f:
            assert f.read().startswith("This is hidden!")
