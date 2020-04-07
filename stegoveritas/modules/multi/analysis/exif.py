
import logging
logger = logging.getLogger('StegoVeritas:Modules:Multi:Analysis:Exif')

import os
import random
import hashlib
import json
import subprocess
from prettytable import PrettyTable

from ....helpers import slugify

def run(multi):
    """Checks for any Exif data in/about the file.

    Args:
        image: MultiHandler class instance

    Returns:
        None

    Saves the result to RESULTSDIR/exif/
    """

    args = multi.veritas.args

    # Nothing to do
    if not args.auto and not args.exif:
        logger.debug('Nothing to do.')
        return

    # Note: Python3.6+ added json.loads support for bytes. Thus using decode for backwards compatibility.
    exif = json.loads(subprocess.check_output(['exiftool', '-j', '-b', multi.veritas.file_name ]).decode())

    table = PrettyTable(['key','value'])
    table.align='l'
    exif_values = []

    for key, value in exif[0].items():
        table.add_row([key, value])
        exif_values.append((key, value))

    print("Exif\n====")
    print(table)

    # Save it out
    save_dir = os.path.join(multi.veritas.results_directory, 'exif')

    os.makedirs(save_dir, exist_ok=True)

    for key,value in exif_values:
        if type(value) in [int, float, bool]:
            value = str(value)

        outfile = os.path.join(save_dir, slugify(key))

        # Slugify means that we might have collisions
        if os.path.exists(outfile):
            logger.warn('Exif outpat already exists, modifying.')
            outfile += '_' + hashlib.md5(str(random.random()).encode()).hexdigest()

        if isinstance(value, list):
            value = ", ".join(str(x) for x in value)

        with open(outfile, 'wb') as f:
            f.write(value.encode())

