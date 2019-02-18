
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
    # TODO: Validate that this analysis should be run (need to propagate default_run value)

    """
    # Nothing to do
    if not image._default_run and not args.meta:
        logger.debug('Nothing to do.')
        return
    """

    exif = json.loads(subprocess.check_output(['exiftool', '-j', multi.veritas.file_name ]))

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
        if type(value) in [int, float]:
            value = str(value)

        outfile = os.path.join(save_dir, slugify(key))

        # Slugify means that we might have collisions
        if os.path.exists(outfile):
            logger.warn('Exif outpat already exists, modifying.')
            outfile += '_' + hashlib.md5(str(random.random()).encode()).hexdigest()

        with open(outfile, 'wb') as f:
            f.write(value.encode())

