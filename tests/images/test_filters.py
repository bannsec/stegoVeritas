
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

from glob import glob
import lzma
import tempfile
import os
import hashlib
import stegoveritas
from stegoveritas.modules.image import SVImage

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

def test_filters_general():

    # Just enumerating an expected run for now
    expected_hashes = ['c35aa2a15d7dbb4d0babc40010c7ee90095e7a19fb9701845207f0cdb7d444ac', '217b46ff1e44859c4ae581cabbd398de0f0c6475379f408727d19cd6ef666f2f', 'ff7d7f737e28be5f3450272205976766c323f88916148e4214cca64d59ef5a82', 'fc505985fe2290a2b4aedad4267e10a54a69727ad2238581f22c76d414732cfd', '96b968a62142498d41288100d93e6090b85cc85d0bb61373399130293137ac31', 'c586a04084a5d311cf9947138b765b40f91e2f62c09f8fb71ab62e31abc08812', 'd00aadadd2f8d6b66c114e1cb393ac6bcb029bbb9d8ca59b9e00c65b48a81cb7', '2fd60df6285a8cd850f2e302ea8486bfbd0560aed7bc02270ce2e5cf5b7beb1a', '87a065c6d1f4cf5f7e1c39081f291c9dfcc615685169d6dc24056a320603acec', '84d829c3a27c7b86331029b0ccfd3a744a258f956f8b3420345963d451a32128', '3cdb1f23dde9c46a3234bc0329216e847f3406fb1ce40efcad1437e529602533', '8f8bf6afafe5f910cc025657055cf4846550b0c9da4ac9c2331c5e34643a0103', '6964ad9716775db61dc74133646cc7426196266bd069fd7da72dbbf31e045838', '6a1f326e969c759799186c01d25d4785cff8fde900728df54f7aab8db5b9dc13', '1d089027b26bf06f76a013fcdc5adae48c71c3e1dd76c1d010771586a87d9347', '35deb8274ff3795275e687848cb8608a8c6aae04d2ed3b10e75c7b956ce0dce2', '7c636d0ce2db36ecfea92fadb4cf678e5226de47c222c25d20640b7496da876f', '72eebe8abaa3b71dd5c5beef0ee45990d56035de557fff54eb7938f1d962bb4c', '3147f3466659f909c30d9691cbed79e0aa93ba7f31cc3de074e3e2c07d7299e8', '1b218642c748f26c4ff7e9993bb8e33ccda1d5cff6cc4c8a5182e3074ea2a146', '99fdc34851cee61dc241176609ece8ef3cb275fc12d704fa28b78aa3532eecb9', 'd81faa671760e1d82c37798330256592e4fc63786e590146ea188f3294075421', 'a654192cd53ffd001c1fbf212d0397fa035b704b0bd88cfd2cac0609a46992ca', '3551bcdb88a63d5d9dd78c649ff4358fb7bd60a1f8a217f81e0f88b6e2082238', 'e87c13762895f46bc378face7f1cbf88e1b15b957d0be35beb7100adbf60d893', '4ce36f55619b1158b4d46cb0f5b3a3ca7d36b8ffd58b96ee02f3745e0285bcc7', 'cbb35153f7423c228ce0f65f807c1c6fa5216801d0fb9f83ede83831277a952f', 'bb5f212d229b2d62146e54a1536f8e00bee36f33c6600ead7aa55c0863df7a40', '1b5b9903efb09541d0e4f3d81ccee203015392ad039d510f0cbb2dab82ecd880', '7ca76b39e0677cda05f3b763c0f5413d394a2a263444dc203a1bfec24a1c7ee3', '33782a4ea7b516d4be6084bba99974cdc01651a0e0dde47bae7e19b94c113fcd', 'e82ac6c7cbd727323e0a7e5fc365d3a93226e132a05fa2c9c1fbe7429c2ef4dc', '30d6055cc8585a1e99d24c14adf0b4901623d2c9c32d9941eceb6272a0f232c1', '16c4822cbcacc29ff4e3f16d6914eb0bb545f2a9b0d990eaed1d52a97452701f', 'a8646064368becf884c7b4f2eb415222a07b8986564ec85588b91eb2b581f284', 'b403509bb2cde5e1b1e12430e07748479aeb6fd7d138365025bc2045c0dcc1f6', '8e2cca5767003620e98041c85e015a922fce507186f3177ab7e29eabf0c96e85', '3da5482c874a55612b076ada6838eadf43308b3a5c9b4655c3714a695398e991', '6fa524057dca871f1cd21e2ea0eefe483ce2757165a133c8306b74a893f32ea9', 'ca30249c54febb404d1b9a17fb5dbdb513f1caf66d0ee2265c66b6004f0f78e3', '4810712f350d70db6a790c94ef26f52ad3ee8a54ec9a7094b0d5b1ce10f2112a', '77ba4e421659b6b63914322d46b09c9b6ee23f51edcfb5d8896908e2d49fc297', 'cdcb907bebdb380e78bde7124395b2a0baca70f059efdc194a9682cdef4a9ca5', 'e3059a40e602dff9f4f69c8ce7feb0361f1955a5e9b8fc0fad5d8b9f95ad2281', '8573391d1e120c5019f65179de4ba151726e318b576005849ed38c20cf1e0b9a', '503064845994c887becb0c77bd0acddc12a4bcfa946ae6069e6766c7845d6675', 'e54561142396959e4e341967b5b6b4b66a8b637a08fa91999ac2b7e00853fa78', 'ffc8b494dfad0793cab88da00fff671527f461ee5e23e035e9ac166ecbbc958d', '135b0a8c0dc2e770419675657b7cb02077d8cc1c28e108d778d17679c5058873', '7dcaf947264e16fd7959b4ab3c23674c87b44bb2fc873a205e84ac6719b4ae4c']

    with tempfile.TemporaryDirectory() as tmpdirname:  
        args = [os.path.join(SCRIPTDIR, 'owl_nosteg.jpg'), '-out', tmpdirname, '-imageTransform'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        _, _, files = next(os.walk(tmpdirname))

        for f in files:
            assert SVImage.hash_file(os.path.join(tmpdirname, f)) in expected_hashes

def test_filters_truncated_image():

    with tempfile.TemporaryDirectory() as tmpdirname:  

        with lzma.open(os.path.join(SCRIPTDIR, 'pico2018-special-logo.bmp.xz'), "rb") as f:
            with open(os.path.join(tmpdirname, 'pico2018-special-logo.bmp'), "wb") as g:
                g.write(f.read())

        args = [os.path.join(tmpdirname, 'pico2018-special-logo.bmp'), '-out', tmpdirname, '-imageTransform'] 
        veritas = stegoveritas.StegoVeritas(args=args)
        veritas.run()

        assert len(glob(os.path.join(tmpdirname, "*"))) > 3
