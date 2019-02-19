
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

def test_extract_frames_apng():

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'Animated_PNG_example_bouncing_beach_ball.png'), '-out', tmpdirname, '-extract_frames'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        frames = glob(os.path.join(tmpdirname, '*_frame_*.png'))

        assert len(frames) == 20

        expected_hashes = ['4984cd34d8f67a060cc3ea0fab8fda80fe32e78e2290d3692d2681657d2674bb', '46bff92f931cf247608bdb68b541d14559e7968969de2192190b0a65f735cde4', 'aab92ada01f7ccd13c5a2c31296385a2bb1cc2e94243f2041aac0808883b5cbe', 'cb5dc80b7f386daf0fffbda763f2c5465036ff38fbb76cd7ecfbcb829824006a', '0b524223c49b671df97dacaa8807acf0fdade046fb2bdd3e7c2309457ca5004f', 'ad6b6c9cbe1f15c803356a4296f94c895c3747aaca8f977a272a83d6ebfdf676', '379f74e77a2a2bf2a27a2d38b109a7b28decf6d577619f4117441afc21b01e6c', 'd4048ecf441fb11402996ccb7f33fbfe2d61e1660d9caa17114c245b44f3a629', 'cc62e051325746579f9fa913766e4b872f790a37b539e6c710d9cb4535f2ad16', '2d8924862326066b46a6abef2aa61e150e6c933f57ec8280b83d8297d05be793', '2619bf1ef0685aa3c9f8745393d43963f9f3c37021c8381ceabeae3038e0af1e', 'fa8db31b7a6ac3b96705d405cd9e3dc04b2b8d1b9dce24219db937c1f4c8ddaa', '3876ab9e1a14a8b15c3e7e1b58474f0c35a9368c0a2dd149a3b226af3cc469c8', 'd94d61882216ae41e212e7e21994cea6ba195964046eb2399723331abefbe3b3', 'ff796a3ca22fca14819ebf0c6722dfa9b1fe7837396257b8fd9d05093398aee6', '622873b75685aa17a060fa5bbb7fc2d3368e9a6260f7394f68ccd01efb6a9a3a', 'a6770e6b857c0d6d34b41c49b96eb9e5cf42a213d042b9c3ff79117bd9b716a2', 'd362b4cf63f2a1012cb0e2d17d3b263843d28136deb340edec4fbc2774e666b0', '4ba41bd812ca08aaec3f60a07ec765ec8937602d53222b7b0fce46b9438a11c3', 'e859f886e3b65ec4e8f6cb14d31f32c36d1a8bf9a276c4f838f76dfae6ddf38d']

        for f in frames:
            assert SVImage.hash_file(os.path.join(tmpdirname, f)) in expected_hashes
