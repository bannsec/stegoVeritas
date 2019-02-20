
import logging
logger = logging.getLogger('StegoVeritas:Modules:Multi:Analysis:Carve')

import os
import random

def run(multi):
    """Carve/extract anything buried in this file.

    Args:
        image: MultiHandler class instance

    Returns:
        None

    Saves the result to RESULTSDIR/keepers/
    """

    args = multi.veritas.args

    # Nothing to do
    if not args.auto and not args.carve:
        logger.debug('Nothing to do.')
        return

    # This is just a thin wrapper to hand the base file off to test_output method
    with open(multi.veritas.file_name, 'rb') as f:
        multi.veritas.test_output(f.read())
