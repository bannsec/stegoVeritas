
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import tempfile
import os
import hashlib
import stegoveritas
from PIL import Image

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_filters_general():

    # Just enumerating an expected run for now
    expected_hashes = ['5ea73552b9c0d7532a62886eb161440e', '97c262ed74095c889e8667e56b2ff5c8', 'dbc6b4ec6570b0dd46ff8c72423eeff0', '0bb301ecb4eff90076fe368029fca566', '5888da97ee74e2c8a35a3684ef6bd0ab', '7cc82ef5611065827ee06e0e092b238e', '36f743851062da8d6c3a57e19f7cc916', 'ff97934cbc5c4575182317390cead82a', '60857262fd7bc06aaec9b220bdf3a8aa', '267bc1032d2c5e4984fe02b7d5508e84', 'd4901f0df46723e1be18a12b427ee5a4', 'e72810325d04f5856160616ad91b536e', 'e7e8ac78fc5327ecf0d2e68b41eeafe4', 'e8d98b061b2c712b230a1791318e582e', '2920122064cd99e65472b2e524d0fb0e', '33a28a657e4b1d1d8d1ad2a7c6ac5994', '43ee26c5a7c55a599ef2c0aa490c8f74', '51fb268810c5158ef44924aca418004f', 'e96afcead1b09d09b1adc970f42982e9', 'a333bf11e1672fea92307281b5a076b0', '46d84d2f46d6dd696792be0327dc6d3c', 'd1daaaad7c20511aa6e7797d7394f3a2', '74e157db8af388856b0abf50bd8d6943', '1ffb34a82093b6d3d7ed78f3a5e1f282', 'b239c9ab357457a3b7bf21dc170aaa15', '65c0828eec00d88868dc87c6999f11a3', '0dd6ed27f157f61c0e605bdf08fb272a', 'daea50e69b777bba62aec2ac1469b3fc', 'c3a85dfb468bf27abd8bab165e2d0e34', '8822ecd5fd954182df7f4152e87a1e5c', '40c20a442c95ece9e9e2a677c98475f5', 'd31d2da30e5d26be7cca3fe08af0e130', '4fecae89510ea0f5fcb93c68e6ba02df', 'fe32f3bdf1c41e22d25d90adce53bb91', '3ce375193349d798674f8108bab5fbc0', '47fd374f57f989bbf95e411a02760290', '0c1252faec1df50a81a460ca1e7010d8', 'cdf61c818fbd8584b5a68a96ca0ba014']

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_nosteg.jpg'), '-out', tmpdirname, '-imageTransform'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))

        for f in files:
            img = Image.open(os.path.join(tmpdirname, f))
            assert hashlib.md5(img.tobytes()).hexdigest() in expected_hashes
