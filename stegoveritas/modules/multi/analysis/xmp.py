
import logging
logger = logging.getLogger('StegoVeritas:Modules:Multi:Analysis:XMP')

import os
import random
import hashlib
import libxmp.utils
from prettytable import PrettyTable

from ....helpers import slugify

def run(multi):
    """Checks for any XMP data in the file.

    Args:
        image: MultiHandler class instance

    Returns:
        None

    Saves the result to RESULTSDIR/xmp/
    """

    args = multi.veritas.args

    # Nothing to do
    if not args.auto and not args.xmp:
        logger.debug('Nothing to do.')
        return

    xmp = libxmp.utils.file_to_dict(multi.veritas.file_name)

    # No XMP data here
    if xmp == {}:
        return

    table = PrettyTable(['key','value'])
    xmp_values = []

    for definition, values in xmp.items():
        for value in values:
            table.add_row([repr(value[0]), repr(value[1])])
            xmp_values.append((value[0], value[1]))

    print("XMPP\n====")
    print(table)

    # Save it out
    save_dir = os.path.join(multi.veritas.results_directory, 'xmp')

    os.makedirs(save_dir, exist_ok=True)

    for key,value in xmp_values:
        outfile = os.path.join(save_dir, slugify(key))

        # Slugify means that we might have collisions
        if os.path.exists(outfile):
            logger.warn('XMP outpath already exists, modifying.')
            outfile += '_' + hashlib.md5(str(random.random()).encode()).hexdigest()

        with open(outfile, 'wb') as f:
            f.write(value.encode())
    

