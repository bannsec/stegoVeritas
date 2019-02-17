
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_lsb_brute_1():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'lsb_red_0.png'), '-out', tmpdirname, '-bruteLSB'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))
        found = False
        for f in files:
            with open(os.path.join(tmpdirname, f),'rb') as f:
                if hashlib.md5(f.read()).hexdigest() == '20ba8aa2da066e371747502079991071':
                    found = True
                    break
        assert found == True
