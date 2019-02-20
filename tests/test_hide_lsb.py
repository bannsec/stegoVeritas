
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas
import subprocess

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_hide_lsb_command_line():

    with tempfile.TemporaryDirectory() as tmpdirname:
        new_steg_file = os.path.join(tmpdirname, 'new_steg.png')
        original_file = os.path.join(SCRIPTDIR, 'images', 'owl_nosteg.jpg')
        hidden_message = 'This is my hidden LSB message!'

        # Create the hidden message
        subprocess.check_output(['stegoveritas_hide_lsb', '-bands', 'R', '-output', new_steg_file, original_file, hidden_message])

        # Find the hidden message
        args = [new_steg_file, '-out', tmpdirname, '-extractLSB', '-red', '0']
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(veritas.results_directory))
        found = False
        for f in files:
            with open(os.path.join(veritas.results_directory, f),'rb') as f:
                if hidden_message.encode() in f.read():
                    found = True
                    break
        assert found == True

